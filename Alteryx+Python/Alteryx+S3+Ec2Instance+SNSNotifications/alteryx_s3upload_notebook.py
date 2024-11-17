from ayx import Alteryx
import boto3
from botocore.config import Config
from botocore import UNSIGNED
import os
import tempfile

# S3 Configuration
BUCKET_NAME = "alteryxetl"  # Replace with your S3 bucket name
OBJECT_NAME = "uploaded/co2analytics.csv"  # File path in the bucket

# Configure the S3 client for unsigned (public) requests
s3 = boto3.client(
    's3',
    config=Config(signature_version=UNSIGNED)  # Force unsigned requests
)

# Upload Function
def upload_file_to_s3(bucket_name, object_name, file_path):
    try:
        # Upload file to S3
        with open(file_path, "rb") as file_data:
            s3.put_object(Bucket=bucket_name, Key=object_name, Body=file_data)
        print(f"File uploaded successfully to {bucket_name}/{object_name}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"Failed to upload file: {str(e)}")

# Main Workflow
try:
    # Read DataFrame from Alteryx input
    df = Alteryx.read("#1")  # Read data from Alteryx input anchor

    # Create a temporary file to save the DataFrame
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as temp_file:
        temp_file_path = temp_file.name
        df.to_csv(temp_file_path, index=False)
        print(f"DataFrame saved temporarily to {temp_file_path}")

    # Upload the temporary file to S3
    upload_file_to_s3(BUCKET_NAME, OBJECT_NAME, temp_file_path)

    # Delete the temporary file after upload
    os.remove(temp_file_path)
    print(f"Temporary file {temp_file_path} deleted successfully.")
except Exception as e:
    print(f"Error in workflow: {str(e)}")
