import json
import boto3
import pandas as pd
from io import BytesIO
from datetime import datetime

def lambda_handler(event, context):
    # Create an S3 client
    s3 = boto3.client('s3')
    
    # Specify your bucket name and folder
    bucket_name = 'educationalnasabucket'
    folder_name = 'mars/'
    
    # Create a sample dataframe (replace this with your actual data)
    data = {
        'Planet': ['Mars', 'Mars', 'Mars', 'Mars'],
        'Feature': ['Olympus Mons', 'Valles Marineris', 'Curiosity Rover', 'Phobos'],
        'Type': ['Volcano', 'Canyon', 'Exploration', 'Moon'],
        'Discovery Date': ['1971', '1971', '2012', '1877']
    }
    df = pd.DataFrame(data)
    
    # Add a timestamp column
    df['Report Generated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Create a BytesIO object to store the Excel file
    excel_file = BytesIO()
    
    # Use ExcelWriter to add more formatting options
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Mars Data', index=False)
        
        # Get the worksheet
        worksheet = writer.sheets['Mars Data']
        
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
    file_name = f'mars_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    
    # Combine folder name and file name for the S3 key
    s3_key = folder_name + file_name
    
    # Upload the file to S3
    s3.put_object(Bucket=bucket_name, Key=s3_key, Body=excel_file.getvalue())
    
    return {
        'statusCode': 200,
        'body': json.dumps(f'Successfully created and uploaded {s3_key} to S3!')
    }
