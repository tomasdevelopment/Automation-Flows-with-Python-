import azure.functions as func
import logging
import pandas as pd
from io import BytesIO
from azure.storage.blob import BlobClient
import os

# Initialize the FunctionApp
app = func.FunctionApp()

# Blob Trigger Function for India
@app.function_name(name="Roar_Blob_Trigger_India")
@app.blob_trigger(arg_name="myblob", path="india-roar-raw/{name}", connection="AzureWebJobsStorage")
def blob_trigger_roar_india(myblob: func.InputStream):
    logging.info(f"Processing blob: Name = {myblob.name}, Size = {myblob.length} bytes")

    # Define load_blob_to_df within the function
    # Define load_blob_to_df within the function
    def load_blob_to_df(blob_data, blob_name):
        try:
            if blob_name.endswith('.csv'):
                logging.info("Detected file type: CSV")
                df = pd.read_csv(BytesIO(blob_data))
            elif blob_name.endswith(('.xls', '.xlsx')):
                logging.info("Detected file type: Excel")
                df = pd.read_excel(BytesIO(blob_data), engine='openpyxl')
            else:
                logging.error(f"Unsupported file type for blob: {blob_name}")
                return None
            logging.info(f"DataFrame loaded with shape: {df.shape}")
            return df
        except Exception as e:
            logging.error(f"Error processing blob content: {str(e)}")
            return None

    # Define upload_csv_to_blob within the function
    def upload_csv_to_blob(df, connection_string, container_name, blob_name):
        try:
            logging.info(f"Uploading to container: {container_name}, blob name: {blob_name}")
            blob_client = BlobClient.from_connection_string(
                conn_str=connection_string,
                container_name=container_name,
                blob_name=blob_name
            )
            csv_data = df.to_csv(index=False, encoding='utf-8').encode()
            blob_client.upload_blob(csv_data, overwrite=True)
            logging.info(f"Successfully uploaded '{blob_name}' to '{container_name}'.")
        except Exception as e:
            logging.error(f"Upload error: {str(e)}")
            raise

    # Define query_roar_reports within the function
    def query_roar_reports(df):
        logging.info(f"Processing DataFrame for India with shape: {df.shape}")
        # Custom processing logic can be added here
        return df

    # Load, process, and upload the DataFrame
    blob_data = myblob.read()
    df = load_blob_to_df(blob_data, myblob.name)
    if df is not None:
        processed_df = query_roar_reports(df)
        connection_string = os.getenv("AzureWebJobsStorage")
        output_blob_name = f"processed/{myblob.name}"
        upload_csv_to_blob(processed_df, connection_string, container_name="all-roar-queried", blob_name=output_blob_name)


# Blob Trigger Function for Latam
@app.function_name(name="Roar_Blob_Trigger_Latam")
@app.blob_trigger(arg_name="myblob", path="latam-roar-raw/{name}", connection="AzureWebJobsStorage")
def blob_trigger_roar_latam(myblob: func.InputStream):
    logging.info(f"Processing blob: Name = {myblob.name}, Size = {myblob.length} bytes")

    # Define load_blob_to_df within the function
    def load_blob_to_df(blob_data, blob_name):
        try:
            if blob_name.endswith('.csv'):
                logging.info("Detected file type: CSV")
                df = pd.read_csv(BytesIO(blob_data))
            elif blob_name.endswith(('.xls', '.xlsx')):
                logging.info("Detected file type: Excel")
                df = pd.read_excel(BytesIO(blob_data), engine='openpyxl')
            else:
                logging.error(f"Unsupported file type for blob: {blob_name}")
                return None
            logging.info(f"DataFrame loaded with shape: {df.shape}")
            return df
        except Exception as e:
            logging.error(f"Error processing blob content: {str(e)}")
            return None

    # Define upload_csv_to_blob within the function
    def upload_csv_to_blob(df, connection_string, container_name, blob_name):
        try:
            logging.info(f"Uploading to container: {container_name}, blob name: {blob_name}")
            blob_client = BlobClient.from_connection_string(
                conn_str=connection_string,
                container_name=container_name,
                blob_name=blob_name
            )
            csv_data = df.to_csv(index=False, encoding='utf-8').encode()
            blob_client.upload_blob(csv_data, overwrite=True)
            logging.info(f"Successfully uploaded '{blob_name}' to '{container_name}'.")
        except Exception as e:
            logging.error(f"Upload error: {str(e)}")
            raise

    # Define query_roar_reports within the function
    def query_roar_reports(df):
        logging.info(f"Processing DataFrame for Latam with shape: {df.shape}")
        # Custom processing logic can be added here
        return df

    # Load, process, and upload the DataFrame
    blob_data = myblob.read()
    df = load_blob_to_df(blob_data, myblob.name)
    if df is not None:
        processed_df = query_roar_reports(df)
        connection_string = os.getenv("connection_string")
       # output_blob_name = f"Latam/{myblob.name}"
        output_blob_name = f"{myblob.name}"
        upload_csv_to_blob(processed_df, connection_string, container_name="all-roar-queried", blob_name=output_blob_name)
