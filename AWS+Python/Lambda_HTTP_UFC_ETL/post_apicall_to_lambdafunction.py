import pandas as pd
import requests
import json
import numpy as np
from tqdm import tqdm

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, float):
            if np.isnan(obj) or np.isinf(obj):
                return None
            if abs(obj) > 1e15:  # Handle very large floats
                return str(obj)
        return super().default(obj)

def preprocess_dataframe(df):
    df = df.replace([np.inf, -np.inf], 1e15)
    float_columns = df.select_dtypes(include=['float64']).columns
    df[float_columns] = df[float_columns].round(6)
    return df

def chunk_dataframe(df, chunk_size=100):
    return [df[i:i+chunk_size] for i in range(0, len(df), chunk_size)]

def process_chunk(chunk, lambda_url):
    chunk_list = chunk.to_dict(orient='records')
    json_data = json.dumps(chunk_list, cls=CustomJSONEncoder)
    response = requests.post(lambda_url, data=json_data, headers={'Content-Type': 'application/json'})
    response.raise_for_status()
    return pd.DataFrame(json.loads(response.text))

# Assuming ufc_df is your DataFrame
# If not, replace this line with your actual DataFrame creation/loading
# ufc_df = pd.read_csv('your_data.csv')

ufc_df = preprocess_dataframe(ufc_df)

lambda_url = "https://123.execute-api.us-east-2.amazonaws.com/default/yourfunctionname"

chunk_size = 100  # Adjust this value based on your data and Lambda limits
chunks = chunk_dataframe(ufc_df, chunk_size)

results = []

try:
    for chunk in tqdm(chunks, desc="Processing chunks"):
        try:
            result_df = process_chunk(chunk, lambda_url)
            results.append(result_df)
        except requests.exceptions.RequestException as e:
            print(f"Error processing chunk: {e}")
            continue

    if results:
        final_result_df = pd.concat(results, ignore_index=True)
        print("Data processed successfully. Final result shape:", final_result_df.shape)
    else:
        print("No data was successfully processed.")

except Exception as e:
    print(f"An unexpected error occurred: {e}")
