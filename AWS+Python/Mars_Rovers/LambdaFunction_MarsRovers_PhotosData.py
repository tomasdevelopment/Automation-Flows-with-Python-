import json
import boto3
import pandas as pd
import requests
from io import BytesIO
from datetime import datetime
import logging
import time

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# NASA API key - consider using AWS Secrets Manager for production
NASA_API_KEY = os.environ.get('Nasa_Api_Key')

def get_rover_manifest(rover_name):
    url = f"https://api.nasa.gov/mars-photos/api/v1/manifests/{rover_name}"
    params = {
        "api_key": NASA_API_KEY
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data['photo_manifest']
        elif response.status_code == 429:
            logger.warning(f"Rate limit hit for {rover_name}. Waiting before retry.")
            time.sleep(5)  # Wait for 5 seconds before retrying
            return get_rover_manifest(rover_name)  # Retry the request
        else:
            logger.error(f"Error fetching data for {rover_name}: Status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred while fetching data for {rover_name}: {e}")
        return None

def process_rover_data(manifest):
    return {
        "Name": manifest['name'],
        "Landing Date": manifest['landing_date'],
        "Launch Date": manifest['launch_date'],
        "Status": manifest['status'],
        "Max Sol": manifest['max_sol'],
        "Max Date": manifest['max_date'],
        "Total Photos": manifest['total_photos'],
        "Latest Sol Photos": manifest['photos'][-1]['total_photos'],
        "Latest Sol Cameras": ", ".join(manifest['photos'][-1]['cameras'])
    }

def lambda_handler(event, context):
    logger.info("Starting lambda function execution")
    try:
        # Create an S3 client
        s3 = boto3.client('s3')
        
        # Specify your bucket name and folder
        bucket_name = 'educationalnasabucket'
        folder_name = 'mars/'
        
        rovers = ["Curiosity", "Opportunity", "Spirit"]
        rover_data = []
        
        logger.info("Fetching rover data from NASA API")
        for rover in rovers:
            manifest = get_rover_manifest(rover)
            if manifest:
                rover_data.append(process_rover_data(manifest))
        
        if rover_data:
            # Create pandas DataFrame
            df = pd.DataFrame(rover_data)
            
            # Create a BytesIO object to store the Excel file
            excel_file = BytesIO()
            
            logger.info("Creating Excel file")
            # Use ExcelWriter to add more formatting options
            with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Rovers_Data', index=False)
                
                # Get the worksheet
                worksheet = writer.sheets['Rovers_Data']
                
                # Adjust column widths
                for column in worksheet.columns:
                    max_length = 0
                    column = [cell for cell in column]
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(cell.value)
                        except:
                            pass
                    adjusted_width = (max_length + 2)
                    worksheet.column_dimensions[column[0].column_letter].width = adjusted_width
            
            # Move the cursor to the beginning of the file
            excel_file.seek(0)
            
            # Generate a unique file name
            file_name = f'mars_rovers_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
            
            # Combine folder name and file name for the S3 key
            s3_key = folder_name + file_name
            
            logger.info(f"Uploading file {s3_key} to S3")
            # Upload the file to S3
            s3.put_object(Bucket=bucket_name, Key=s3_key, Body=excel_file.getvalue())
            
            logger.info("Lambda function execution completed successfully")
            return {
                'statusCode': 200,
                'body': json.dumps(f'Successfully created and uploaded {s3_key} to S3!')
            }
        else:
            logger.error("No rover data was retrieved")
            return {
                'statusCode': 500,
                'body': json.dumps('Failed to retrieve rover data')
            }
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'An error occurred: {str(e)}')
        }
