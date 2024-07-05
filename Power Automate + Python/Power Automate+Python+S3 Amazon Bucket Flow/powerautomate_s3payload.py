import pandas as pd
import requests
import json
import base64
from io import BytesIO

# Sample DataFrame
data = {
    'company_country': ['USA', 'Canada', 'Mexico'],
    'company_number_of_employees': [100, 200, 150],
    'company_sector_id': [1, 2, 3]
}
sample_df = pd.DataFrame(data)
print("test_df:")
print(sample_df)

# Function to save DataFrame to an in-memory Excel file
def save_df_to_buffer(df):
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    buffer.seek(0)
    return buffer

# Function to encode file content to base64
def encode_file_to_base64(buffer):
    file_content = buffer.read()
    return base64.b64encode(file_content).decode('utf-8')

# Convert DataFrame to Excel and encode to base64
excel_buffer = save_df_to_buffer(sample_df)
encoded_excel = encode_file_to_base64(excel_buffer)
file_name = "sample_data.xlsx"

# Create the JSON payload with base64-encoded Excel and file name
json_payload = json.dumps({
    "file_content": encoded_excel,
    "file_name": file_name
})
print("JSON Payload:")
print(json_payload)

# Define the URL for the automate flow
url = 'https://prod-142.westus.logic.azure.com/workflows/c2fe29240204403bb662356128760e93/triggers/manual/paths/invoke/{JSON}?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=npKk7lyBoVn30QigywtgBglQj2Z88hwpQJGsFkr12398'

# Headers for the POST request
headers = {
    'Content-Type': 'application/json'
}

# Make the POST request
response = requests.post(url, headers=headers, data=json_payload)

# Check the response
if response.status_code == 200:
    response_data = response.json()  # Assuming the response is in JSON format
    response_df = pd.DataFrame(response_data)
    print("Response Data:")
    print(response_df)

    # Merge the response data with the original DataFrame
    merged_df = sample_df.merge(response_df, on='company_sector_id', how='left')
    print("Merged DataFrame:")
    print(merged_df)
else:
    print(f'Failed to get a valid response. Status code: {response.status_code}')
    print(response.text)
