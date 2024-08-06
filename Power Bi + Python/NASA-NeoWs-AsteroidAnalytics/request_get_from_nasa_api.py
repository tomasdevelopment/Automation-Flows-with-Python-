import requests
import pandas as pd
from datetime import datetime, timedelta

def get_neo_data(api_key, start_date, end_date):
    url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={start_date}&end_date={end_date}&api_key={api_key}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        # Extract asteroid data
        neo_data = []
        for date, asteroids in data['near_earth_objects'].items():
            for asteroid in asteroids:
                neo_data.append({
                    'Date': date,
                    'ID': asteroid['id'],
                    'Name': asteroid['name'],
                    'Diameter_Min_KM': asteroid['estimated_diameter']['kilometers']['estimated_diameter_min'],
                    'Diameter_Max_KM': asteroid['estimated_diameter']['kilometers']['estimated_diameter_max'],
                    'Is_Potentially_Hazardous': asteroid['is_potentially_hazardous_asteroid'],
                    'Close_Approach_Date': asteroid['close_approach_data'][0]['close_approach_date'],
                    'Miss_Distance_KM': float(asteroid['close_approach_data'][0]['miss_distance']['kilometers']),
                    'Relative_Velocity_KMH': float(asteroid['close_approach_data'][0]['relative_velocity']['kilometers_per_hour'])
                })
        
        df = pd.DataFrame(neo_data)
        return df
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return pd.DataFrame()

# Your API key
api_key = '123' #the api key your eceive after visiting the nasa api webiste using your browser

# Set date range (API limits to 7 days per request)
end_date = datetime.now().strftime('%Y-%m-%d')
start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

# Get the data
neo_df = get_neo_data(api_key, start_date, end_date)

# Print the first few rows and column names for verification
print(neo_df.head())
print("\nColumns:")
print(neo_df.columns)

# Return the DataFrame for Power BI
neo_df
