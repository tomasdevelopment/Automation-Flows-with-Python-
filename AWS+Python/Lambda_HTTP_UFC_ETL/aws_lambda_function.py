import json
import pandas as pd



def filter_ufc_winners(df):
    df = df.copy()
    df.columns = df.columns.str.lower()
    # Debugging: Print original columns
    print("Original columns:", df.columns)
    
    winners = df[((df['winner'] == 'Red') & (df['r_fighter'] == df['r_fighter'])) |
                 ((df['winner'] == 'Blue') & (df['b_fighter'] == df['b_fighter']))]
    
    relevant_columns = ['referee', 'date', 'location', 'winner', 'title_bout', 'weight_class', 'country']
    
    # Create winner_name column
    winners['winner_name'] = winners.apply(lambda row: row['r_fighter'] if row['winner'] == 'Red' else row['b_fighter'], axis=1)
    
    # Extract country from location
   
    
    # Filter title bouts only
    winners = winners[winners['title_bout'] == True]
    
    # Copy relevant columns
    result = winners[relevant_columns].copy()
    
    # Debugging: Print result DataFrame before returning
    print("Result DataFrame:")
    print(result.head())
    
    return result

def lambda_handler(event, context):
    try:
        # Parse the incoming data
        body = json.loads(event['body'])
        
        # Create DataFrame from the parsed body
        df = pd.DataFrame(body)
        
        # Filter winners and include only relevant columns
        winner_df = filter_ufc_winners(df)
        
        # Debugging: Print winner_df to confirm country column exists
        print("Winner DataFrame with 'country' column:")
        print(winner_df.head())
        
        if winner_df.empty:
            return {
                'statusCode': 200,
                'body': json.dumps({'message': 'No winners found in the provided data.'}),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                    'Access-Control-Allow-Methods': 'OPTIONS, POST, GET'
                }
            }
        
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
    except json.JSONDecodeError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid JSON in request body'}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                'Access-Control-Allow-Methods': 'OPTIONS, POST, GET'
            }
        }
    except KeyError as e:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': f'Missing required field: {str(e)}'}),
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
            'body': json.dumps({'error': f'An unexpected error occurred: {str(e)}'}),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                'Access-Control-Allow-Methods': 'OPTIONS, POST, GET'
            }
        }
