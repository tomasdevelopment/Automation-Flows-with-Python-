#Based on the returned data from the lambda, additional anaysis you can maek
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

# Create the choropleth map
fig = px.choropleth(winners_data, 
                    locations='iso_alpha', 
                    color='winner_count',
                    hover_name='country',
                    color_continuous_scale=px.colors.sequential.Plasma,
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

# If the choropleth doesn't work, try a scatter_geo plot as an alternative
fig_scatter = px.scatter_geo(winners_data,
                             locations='iso_alpha',
                             color='winner_count',
                             hover_name='country',
                             size='winner_count',
                             projection='natural earth',
                             title='UFC Title Bout Winners by Country (Scatter)')

