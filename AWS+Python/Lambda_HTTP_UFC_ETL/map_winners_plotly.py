import pandas as pd
import plotly.express as px

# [Your existing data loading and processing code remains the same]

# Create a dictionary mapping countries to ISO alpha-3 codes
country_code_map = {
    'USA': 'USA', 'Brazil': 'BRA', 'Canada': 'CAN', 'Australia': 'AUS',
    'England': 'GBR', 'Japan': 'JPN', 'Mexico': 'MEX', 'Germany': 'DEU',
    'United Arab Emirates': 'ARE', 'Singapore': 'SGP', 'China': 'CHN',
    'Russia': 'RUS', 'United Kingdom': 'GBR', 'Netherlands': 'NLD',
    'New Zealand': 'NZL', 'South Korea': 'KOR', 'Sweden': 'SWE',
    # Add more mappings as needed
}

# Add ISO alpha-3 country codes
winners_data['iso_alpha'] = winners_data['country'].map(country_code_map)

# Print the data with ISO codes for debugging
print("\nData with ISO codes:")
print(winners_data)

# Check if iso_alpha column was created successfully
if 'iso_alpha' in winners_data.columns:
    print("\nISO Alpha codes successfully added.")
    location_column = 'iso_alpha'
else:
    print("\nWarning: ISO Alpha codes could not be added. Using 'country' column instead.")
    location_column = 'country'

# Print unique values in the location column
print(f"\nUnique values in the {location_column} column:")
print(winners_data[location_column].unique())

# Define the color scale
color_scale = [
    (0, "red"),
    (0.5, "yellow"),
    (1, "green")
]

# Create the choropleth map
fig = px.choropleth(winners_data, 
                    locations=location_column, 
                    color='winner_count',
                    hover_name='country',
                    color_continuous_scale=color_scale,
                    title='UFC Title Bout Winners by Country')

# Update the layout for better visibility
fig.update_layout(
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type='equirectangular'
    )
)

fig.show()

# Create a scatter_geo plot
fig_scatter = px.scatter_geo(winners_data,
                             locations=location_column,
                             color='winner_count',
                             hover_name='country',
                             size='winner_count',
                             size_max=50,
                             color_continuous_scale=color_scale,
                             projection='natural earth',
                             title='UFC Title Bout Winners by Country (Scatter)')

# Update marker size to make all points larger
fig_scatter.update_traces(marker=dict(sizemin=10))

fig_scatter.show()
