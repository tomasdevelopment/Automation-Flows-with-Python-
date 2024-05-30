
import requests
import json
import base64
import pandas as pd

##Done to send an email from a python notebook attachement. 
#using a flow with manual trigger and email configuration. Two steps.

# Load the Excel file into a DataFrame (if necessary)
MissingTime = pd.read_excel("/work/Missing Time/MissingTest.xlsx")

def send_data_to_flow(flow_url, file_path):
    try:
        # Open the file and read contents
        with open(file_path, "rb") as file:
            file_content = base64.b64encode(file.read()).decode('utf-8')
        
        # Extract the file name from the path to keep things dynamic and accurate
        file_name = file_path.split('/')[-1]  # This will extract 'MissingTest.xlsx' from the path
        
        # Prepare the data dictionary with the file content and name
        data = {
            "file_content": file_content,
            "file_name": file_name  # Use the dynamically extracted name
        }
        
        # Set the headers to indicate JSON content type
        headers = {'Content-Type': 'application/json'}
        
        # Make the POST request to the Power Automate HTTP trigger URL
        response = requests.post(flow_url, headers=headers, data=json.dumps(data))
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Print the status code and response text to verify success
        print(f"Status Code: {response.status_code}, Response: {response.text}")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response content: {response.content}")
    except Exception as err:
        print(f"Other error occurred: {err}")

# Use the complete flow identifier for the URL
flow_url = 'https://prod-70.<addregionhere>.logic.azure.com:443/workflows/123/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=YnXfg-xm3x9rcmt-0cG4Tz2UqyJwgy5VCTbtpv5iGAk'
send_data_to_flow(flow_url, '/work/Missing Time/MissingTest.xlsx')
