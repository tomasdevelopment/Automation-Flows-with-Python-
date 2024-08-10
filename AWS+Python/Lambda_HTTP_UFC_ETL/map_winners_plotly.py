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

# Sort the data by winner_count to determine color scale breakpoints
winners_data_sorted = winners_data.sort_values('winner_count')
max_count = winners_data_sorted['winner_count'].max()
brazil_count = winners_data_sorted[winners_data_sorted['country'] == 'Brazil']['winner_count'].values[0]

# Define a more gradual color scale
color_scale = [
    (0, "red"),
    (0.9, "yellow"),
    (1, "green")
]

# Create the choropleth map
fig_choropleth = px.choropleth(
    winners_data,
    locations='iso_alpha',
    color='winner_count',
    hover_name='country',
    color_continuous_scale=color_scale,
    range_color=[0, max_count],
    title='UFC Title Bout Winners by Country (Choropleth)'
)

# Update the layout for better visibility
fig_choropleth.update_layout(
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type='natural earth'
    )
)
fig.update_layout(
    coloraxis_colorbar=dict(
        title='Winner Count',
        tickvals=[0, max_count/2, max_count],
        ticktext=['0', f'{int(max_count/2)}', str(max_count)]
    )
)

# Create a scatter_geo plot
fig_scatter = px.scatter_geo(
    winners_data,
    locations='iso_alpha',
    color='winner_count',
    hover_name='country',
    size='winner_count',
    size_max=50,
    color_continuous_scale=color_scale,
    range_color=[0, max_count],
    projection='natural earth',
    title='UFC Title Bout Winners by Country (Scatter)'
)

# Update marker size to make all points larger
fig_scatter.update_traces(marker=dict(sizemin=10))

# Update color bar
for fig in [fig_choropleth, fig_scatter]:
    fig.update_layout(
        coloraxis_colorbar=dict(
            title='Winner Count',
            tickvals=[0, brazil_count, max_count],
            ticktext=['0', f'Brazil ({brazil_count})', str(max_count)]
        )
    )

# Show the plots
fig_choropleth.show()
fig_scatter.show()
