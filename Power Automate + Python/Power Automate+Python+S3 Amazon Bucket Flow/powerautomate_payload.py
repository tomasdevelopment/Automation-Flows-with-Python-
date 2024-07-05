import pandas as pd
import requests
import json

# Sample DataFrame
data = {
    'company_country': ['USA', 'Canada', 'Mexico'],
    'company_number_of_employees': [100, 200, 150],
    'company_sector_id': [1, 2, 3]
}
sample_df = pd.DataFrame(data)
print("Sample DataFrame:")
print(sample_df)

# Convert DataFrame to JSON
json_data = sample_df.to_json(orient='records')
print("JSON Data:")
print(json_data)

# Define the URL for the automate flow
url = 'https://prod-142.westus.logic.azure.com/workflows/c2fe29240204403bb662356128760e93/triggers/manual/paths/invoke/{JSON}?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&123'

# Headers for the POST request
headers = {
    'Content-Type': 'application/json'
}

# Make the POST request
response = requests.post(url, headers=headers, data=json_data)

# Fake response data for testing purposes
# fake_response_data = [
#     {"company_sector_id": 1, "sector_name": "Technology"},
#     {"company_sector_id": 2, "sector_name": "Healthcare"},
#     {"company_sector_id": 3, "sector_name": "Finance"}
# ]

# Check the response
if response.status_code == 200 or True:  # Use 'or True' to ensure the fake response is used
    # If using the actual response, you would convert response.content to DataFrame
    # response_data = pd.read_excel(BytesIO(response.content))
    
    # For testing, we use the fake response data
    response_data = pd.DataFrame(response)
    print("Response Data:")
    print(response_data)

    # Merge the response data with the original DataFrame
    merged_df = sample_df.merge(response_data, on='company_sector_id', how='left')
    print("Merged DataFrame:")
    print(merged_df)
else:
    print(f'Failed to get a valid response. Status code: {response.status_code}')
    print(response.text)
