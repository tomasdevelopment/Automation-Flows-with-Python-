import json
import pandas as pd
import boto3
import logging
import os

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('UFCFightData')  # Replace with your table name

# Get the API key from environment variables
API_KEY = os.environ.get('api_key_ufc')
def lambda_handler(event, context):
    try:
        # Check for API key in the authorization header
        headers = event.get('headers', {})
        auth_header = headers.get('Authorization', '')
        
        if not auth_header.startswith('Bearer ') or auth_header.split(' ')[1] != API_KEY:
            logger.warning("Unauthorized access attempt")
            return {
                'statusCode': 401,
                'body': json.dumps({'error': 'Unauthorized'}),
                'headers': {'Content-Type': 'application/json'}
            }

        # Parse the incoming JSON data
        data = json.loads(event['body'])
        
        # Convert the data to a DataFrame
        df = pd.DataFrame(data)
        
        # Validate input data
        required_columns = ['B_age', 'R_age', 'R_fighter', 'B_fighter', 'Referee', 'date', 'location', 'Winner', 'title_bout', 'weight_class']
        if not all(col in df.columns for col in required_columns):
            raise ValueError("Missing required columns in input data")
        
        # Select the required columns
        filtered_df = df[required_columns]
        
        # Calculate age difference for title bouts
        filtered_df['age_difference'] = filtered_df.apply(lambda row: abs(row['B_age'] - row['R_age']) if row['title_bout'] else None, axis=1)
        
        # Enrich data with win streaks (simplified example)
        filtered_df['B_win_streak'] = filtered_df.groupby('B_fighter')['Winner'].apply(lambda x: (x == x.shift()).cumsum())
        filtered_df['R_win_streak'] = filtered_df.groupby('R_fighter')['Winner'].apply(lambda x: (x == x.shift()).cumsum())
        
        # Store processed data in DynamoDB
        with table.batch_writer() as batch:
            for _, row in filtered_df.iterrows():
                batch.put_item(Item=row.to_dict())
        
        # Convert DataFrame to JSON
        result_json = filtered_df.to_json(orient='records')
        
        logger.info(f"Processed {len(filtered_df)} records successfully")
        
        return {
            'statusCode': 200,
            'body': result_json,
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    except Exception as e:
        logger.error(f"Error processing data: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
