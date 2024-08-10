import json
import pandas as pd
import numpy as np

def lambda_handler(event, context):
    try:
        # Parse the incoming data
        body = json.loads(event['body'])
        
        # Create DataFrame from the parsed body
        df = pd.DataFrame(body)
        
        # Convert all column names to lowercase
        df.columns = df.columns.str.lower()
        
        # List of columns we want to keep
        columns_to_keep = ['r_fighter', 'b_fighter', 'winner', 'date', 'weight_class']
        
        # Filter the DataFrame to keep only the specified columns
        df_filtered = df[columns_to_keep]
        
        # Handle NaN, Infinity, and -Infinity values
        df_filtered = df_filtered.replace([np.inf, -np.inf], np.nan)
        
        # Convert DataFrame to a dictionary, handling NaN values
        result_dict = df_filtered.where(pd.notnull(df_filtered), None).to_dict(orient='records')
        
        # Use custom JSON encoder to handle any remaining special float values
        class CustomJSONEncoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, float):
                    if np.isnan(obj) or np.isinf(obj):
                        return None
                return super().default(obj)
        
        return {
            'statusCode': 200,
            'body': json.dumps(result_dict, cls=CustomJSONEncoder),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                'Access-Control-Allow-Methods': 'OPTIONS, POST, GET'
            }
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                'Access-Control-Allow-Methods': 'OPTIONS, POST, GET'
            }
        }
