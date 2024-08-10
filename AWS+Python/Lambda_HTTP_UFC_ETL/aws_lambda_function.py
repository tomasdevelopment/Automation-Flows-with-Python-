import json
import pandas as pd

def filter_ufc_winners(df):
    # Create a copy of the DataFrame to avoid modifying the original
    df = df.copy()
    
    # Ensure all column names are lowercase
    df.columns = df.columns.str.lower()
    
    # Get only the winners
    winners = df[((df['winner'] == 'Red') & (df['r_fighter'] == df['r_fighter'])) | 
                 ((df['winner'] == 'Blue') & (df['b_fighter'] == df['b_fighter']))]
    
    # Create a list of all winners
    all_winners = winners['r_fighter'].where(winners['winner'] == 'Red', winners['b_fighter']).unique()
    
    # Initialize the result DataFrame
    result = pd.DataFrame({'fighter': all_winners})
    
    return result

def lambda_handler(event, context):
    try:
        # Parse the incoming data
        body = json.loads(event['body'])
        
        # Create DataFrame from the parsed body
        df = pd.DataFrame(body)
        
        # Filter winners
        winner_df = filter_ufc_winners(df)
        
        # Convert DataFrame to a dictionary
        result_dict = winner_df.to_dict(orient='records')
        
        return {
            'statusCode': 200,
            'body': json.dumps(result_dict),
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
