import boto3
import pandas as pd
from io import BytesIO
import time

# AWS S3 Configuration
BUCKET_NAME = "alteryxetl"
UPLOAD_FOLDER = "uploaded/"  # Folder where Alteryx uploads files
APPROVED_FOLDER = "approved/"
REJECTED_FOLDER = "rejected/"

# SNS Configuration
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:789873626066:alteryxreview"

# Initialize AWS Clients
s3 = boto3.client("s3")
sns = boto3.client("sns")


def list_s3_files(bucket_name, prefix):
    """List files in a specific S3 folder."""
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    return [obj["Key"] for obj in response.get("Contents", [])] if "Contents" in response else []


def download_s3_file(bucket_name, s3_key):
    """Download a file from S3."""
    response = s3.get_object(Bucket=bucket_name, Key=s3_key)
    return response["Body"].read()


def process_blob(blob_data, blob_name):
    """Load file into a DataFrame based on its extension."""
    try:
        if blob_name.endswith(".csv"):
            print(f"Detected file type: CSV for {blob_name}")
            df = pd.read_csv(BytesIO(blob_data))
            return df, APPROVED_FOLDER
        elif blob_name.endswith((".xls", ".xlsx")):
            print(f"Detected file type: Excel for {blob_name}")
            df = pd.read_excel(BytesIO(blob_data), engine="openpyxl")
            return df, REJECTED_FOLDER
        else:
            print(f"Unsupported file type for: {blob_name}")
            return None, None
    except Exception as e:
        print(f"Error processing file {blob_name}: {e}")
        return None, None


def upload_to_s3(df, folder, file_name, bucket_name):
    """Upload the DataFrame as a CSV back to S3."""
    try:
        csv_buffer = BytesIO()
        df.to_csv(csv_buffer, index=False)
        s3_key = f"{folder}{file_name}"
        s3.put_object(Bucket=bucket_name, Key=s3_key, Body=csv_buffer.getvalue())
        print(f"Uploaded {file_name} to {folder} in bucket {bucket_name}")
    except Exception as e:
        print(f"Failed to upload {file_name}: {e}")


def send_sns_notification(file_name, folder):
    """Send an SNS notification about the processed file."""
    try:
        message = f"File {file_name} has been processed and uploaded to {folder}."
        response = sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject="File Processed Notification"
        )
        print(f"SNS notification sent for {file_name}: {response['MessageId']}")
    except Exception as e:
        print(f"Failed to send SNS notification: {e}")


def process_and_upload_files():
    """Monitor S3 for new files, process them, and upload results."""
    processed_files = set()  # Keep track of processed files

    while True:
        print("Checking for new files...")
        file_keys = list_s3_files(BUCKET_NAME, UPLOAD_FOLDER)

        for file_key in file_keys:
            file_name = file_key.split("/")[-1]

            # Skip already processed files
            if file_name in processed_files:
                continue

            print(f"Processing new file: {file_name}")

            # Download file
            blob_data = download_s3_file(BUCKET_NAME, file_key)

            # Process the file
            df, folder = process_blob(blob_data, file_name)
            if df is None or folder is None:
                continue

            # Upload processed file to the appropriate folder
            upload_to_s3(df, folder, file_name, BUCKET_NAME)

            # Send SNS notification (optional)
            send_sns_notification(file_name, folder)

            # Add to processed files
            processed_files.add(file_name)

        time.sleep(60)  # Check every 60 seconds


# Main Execution
if __name__ == "__main__":
    process_and_upload_files()
