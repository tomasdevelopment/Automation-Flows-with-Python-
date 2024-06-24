import pandas as pd
import json
import requests
import base64

# Function to read and display the Excel file to ensure it exists and can be read properly
def read_excel_file(file_path):
    try:
        df = pd.read_excel(file_path, sheet_name=None)  # Read all sheets
        print("File read successfully.")
        return df
    except Exception as e:
        print(f"Error reading the Excel file: {e}")
        return None

# Function to save multiple DataFrames to a single Excel file
def save_dataframes_to_excel(file_path, df_dict):
    with pd.ExcelWriter(file_path) as writer:
        for sheet_name, df in df_dict.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    print(f"DataFrames saved to {file_path} successfully.")

# Function to encode file content to base64
def encodebase_64(file_path):
    with open(file_path, 'rb') as file:
        file_content = file.read()
    return base64.b64encode(file_content).decode('utf-8')

# Function to convert DataFrame to a semicolon-separated string of email addresses
def dataframe_to_email_string(df):
    email_list = df['Manager Email'].tolist()
    return ";".join(email_list)

# Function to send the Excel data to the Power Automate flow
def send_data_to_flow(flow_url, json_data):
    try:
        # Set the headers to indicate JSON content type
        headers = {'Content-Type': 'application/json'}

        # Make the POST request to the Power Automate HTTP trigger URL
        response = requests.post(flow_url, headers=headers, json=json_data)

        # Check if the request was successful
        response.raise_for_status()

        # Print the status code and response text to verify success
        print(f"Status Code: {response.status_code}, Response: {response.text}")
        return response.text
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response content: {response.content}")
    except Exception as err:
        print(f"Other error occurred: {err}")

def merge_dataframes_from_vendors(sheets_dict, vdf):
    # Set to collect vendor emails
    vendor_emails = set()

    # Check for required columns in vdf first to avoid repeated checking in the loop
    if not {'VendorName', 'VendorEmail'}.issubset(vdf.columns):
        print("Required columns are missing in the vendor dataframe.")
        return pd.DataFrame(columns=['Vendor Email'])

    for sheet_name, df in sheets_dict.items():
        # Ensure the necessary columns are present in the sheet DataFrame
        if "Vendor" not in df.columns:
            print(f"Required 'Vendor' column is missing in sheet {sheet_name}.")
            continue

        try:
            # Merge the DataFrames on the "Vendor" column from df and "VendorName" column from vdf
            merged_df = pd.merge(df, vdf[['VendorName', 'VendorEmail']], left_on='Vendor', right_on='VendorName', how='left')

            # Use the existing 'VendorEmail' column directly
            merged_df['Vendor Email'] = merged_df['VendorEmail']

            # Drop rows where "Vendor Email" is NaN and update unique emails
            vendor_emails.update(merged_df['Vendor Email'].dropna().unique())

        except Exception as e:
            print(f"An error occurred while processing sheet {sheet_name}: {e}")

    # Convert the set to a DataFrame
    final_df = pd.DataFrame(list(vendor_emails), columns=['Vendor Email'])
    print("DataFrames from all sheets merged and processed successfully.")
    return final_df

# Read the original Excel file into a dictionary of DataFrames
original_file_path = "/work/MainReport.xlsx"
sheets_dict = read_excel_file(original_file_path)

# Assuming hcdataset is already defined and available

if sheets_dict is not None:
    # Get unique manager emails
    # Define the sheet names you want to process
    sheet_names = ['report1', 'report2', 'report3']

    # Filter sheets_dict to only include the relevant sheets
    filtered_sheets_dict = {k: v for k, v in sheets_dict.items() if k in sheet_names}

    # Call the function to merge dataframes
    recipients_df = merge_dataframes_from_vendors(filtered_sheets_dict, hcdataset)
    
    if recipients_df is not None:
        print(recipients_df.head())

     
        # Encode the combined file to base64
        combined_base64 = encodebase_64(combined_file)

        # Convert the recipients DataFrame to a semicolon-separated string
        recipients_string = dataframe_to_email_string(recipients_df)
        #mock

        # Convert the recipients string to a JSON structure
        recipientsemail_json = json.dumps({"recipients": recipients_string})

        print("Files created successfully.")

        # Prepare the JSON payload
        payload = {
            "file1_content": combined_base64,
            "file1_name": "finalreport.xlsx",
            "file2_content": recipientsemail_json,
            "file2_name": "email_recipients.json"
        }

        flow_url = 'https://prod-14.westus.logic.azure.com:123/workflows/123/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.123&sig=123-9oGJh-123'
        
        # Send the JSON payload to the Power Automate flow
        response = send_data_to_flow(flow_url, payload)
        if response:
            print(f"Response from Power Automate: {response}")
else:
    print("Failed to read the original Excel file or ")
