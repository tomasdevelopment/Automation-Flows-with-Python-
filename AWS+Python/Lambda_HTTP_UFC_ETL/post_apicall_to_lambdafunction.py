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

def chunk_dataframe(df, chunk_size=10000):
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

lambda_url = "https://h44r98a9tg.execute-api.us-east-2.amazonaws.com/default/On_Demand_Data_Retrieval_API"

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

winners_data = final_result_df
winners_data

import pandas as pd
import plotly.express as px

def process_and_visualize_data(winners_data):
    # Create a dictionary mapping countries to ISO alpha-3 codes
    country_code_map = {
        'USA': 'USA', 'Brazil': 'BRA', 'Canada': 'CAN', 'Australia': 'AUS',
        'England': 'GBR', 'Japan': 'JPN', 'Mexico': 'MEX', 'Germany': 'DEU',
        'United Arab Emirates': 'ARE', 'Singapore': 'SGP', 'China': 'CHN',
        'Russia': 'RUS', 'United Kingdom': 'GBR', 'Netherlands': 'NLD',
        'New Zealand': 'NZL', 'South Korea': 'KOR', 'Sweden': 'SWE',
        'Denmark': 'DNK', 'Uruguay': 'URY', 'Czech Republic': 'CZE',
        'Argentina': 'ARG', 'Chile': 'CHL', 'Poland': 'POL',
        'Croatia': 'HRV', 'Ireland': 'IRL', 'Philippines': 'PHL',
        'Puerto Rico': 'PRI'
    }

    # Extract country from location and add ISO alpha-3 country codes
    winners_data['country'] = winners_data['location'].apply(lambda x: x.split(', ')[-1] if ', ' in x else x)
    winners_data['iso_alpha'] = winners_data['country'].map(country_code_map)
    
    # Handle countries not in the mapping
    if winners_data['iso_alpha'].isna().any():
        missing_countries = winners_data[winners_data['iso_alpha'].isna()]['country'].unique()
        print(f"Warning: The following countries are not in the mapping: {missing_countries}")
    
    # Aggregate data by ISO country code
    aggregation = winners_data.groupby('iso_alpha').agg(
        title_bout_fights_won=('winner', 'count')
    ).reset_index()
    
    # Merge aggregated data back into the original DataFrame
    winners_data = winners_data.merge(aggregation, on='iso_alpha', how='left')
    
    # Handle NaN values in 'title_bout_fights_won' column
    winners_data['title_bout_fights_won'].fillna(0, inplace=True)
    
    # Define a more gradual color scale
    color_scale = [
        (0, "red"),
        (0.9, "yellow"),
        (1, "green")
    ]
    
    # Define a dark theme
    dark_theme = dict(
        plot_bgcolor="rgb(30,30,30)",
        paper_bgcolor="rgb(20,20,20)",
        font=dict(color="white"),
        geo=dict(
            bgcolor="rgb(30,30,30)",
            lakecolor="rgb(30,30,30)",
            landcolor="rgb(50,50,50)",
            subunitcolor="rgb(60,60,60)",
        )
    )
    
    max_count = winners_data['title_bout_fights_won'].max()
    min_count = winners_data['title_bout_fights_won'].min()

    # Create choropleth map
    fig_choropleth = px.choropleth(
        winners_data,
        locations='iso_alpha',
        color='title_bout_fights_won',
        color_continuous_scale=color_scale,
        projection='natural earth',
        title='UFC Title Bout Winners by Country'
    )
    
    # Create scatter plot
    fig_scatter = px.scatter_geo(
        winners_data,
        locations='iso_alpha',
        color='title_bout_fights_won',
        hover_name='country',
        size='title_bout_fights_won',
        size_max=35,
        color_continuous_scale=color_scale,
        range_color=[min_count, max_count],
        projection='natural earth',
        title='UFC Title Bout Winners by Country (Scatter)'
    )
    
    # Apply dark theme to both figures
    for fig in [fig_choropleth, fig_scatter]:
        fig.update_layout(
            dark_theme,
            coloraxis_colorbar=dict(
                title='Title Bouts Won',
                tickvals=[min_count, max_count],
                ticktext=[str(min_count), str(max_count)],
                title_font=dict(color="white"),
                tickfont=dict(color="white"),
            )
        )
    
    # Additional updates for the choropleth map
    fig_choropleth.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor="rgb(100,100,100)",
            countrycolor="rgb(80,80,80)",
        )
    )
    
    # Additional updates for the scatter plot
    fig_scatter.update_layout(
        title=dict(
            text='UFC Title Bout Winners Count by Country (1994-2021)',
            x=0.5,
            xanchor='center',
            font=dict(
                family="Arial Bold",
                size=40,
                color='White',
            )
        )
    )
    
    # Update marker colors for better visibility on dark background
    fig_scatter.update_traces(
        marker=dict(
            line=dict(width=1, color='rgb(150,150,150)'),
            sizemin=10
        )
    )
    
    # Show the figures
    fig_choropleth.show()
    fig_scatter.show()
process_and_visualize_data(winners_data)
