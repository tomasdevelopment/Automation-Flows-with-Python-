![Alt text](3dgraph.png)


Python and Power BI Integration for ETL
Overview
This guide demonstrates how to integrate Python with Power BI to pull data from an API that requires authorization headers, such as NASA’s asteroid data API. This process includes data extraction, transformation, and loading (ETL) steps to show Python’s capability to extend Power BI’s functionality.

Prerequisites
API Key: Obtain your API key from the NASA API portal.
Python Libraries: Ensure you have libraries like requests and pandas installed.
Power BI Desktop: Install Power BI Desktop for running Python scripts.
Step 1: Get Data from NASA API

Obtain API Key: Go to NASA API Portal and sign up for an API key if you haven’t already.

Python Script to Fetch Data:
Create a Python script to fetch data using the API key. Here’s a sample script:

python
Copy code
import requests
import pandas as pd

# Replace 'YOUR_API_KEY' with your actual NASA API key
api_key = 'YOUR_API_KEY'
url = f'https://api.nasa.gov/neo/rest/v1/neo/browse?api_key={api_key}'

response = requests.get(url)
data = response.json()

# Extract data and convert to DataFrame
asteroids = pd.json_normalize(data['near_earth_objects'])
This script retrieves asteroid data from NASA and normalizes it into a DataFrame.

Step 2: Apply Transformations
In Power BI, you can apply transformations to the data retrieved by Python. Here’s how:

Load Data into Power BI:

Open Power BI Desktop.
Go to Home -> Get Data -> Python script.
Run Python Script:

Paste the Python script into the editor and click OK.
Ensure all required libraries are installed in your Python environment.
Transform Data:

After loading, you’ll see the data as a DataFrame in Power BI.
Apply necessary transformations such as filtering, normalization, and creating calculated columns.
For example, in the Python script, you could apply transformations like:

python
Copy code
# Additional transformations
asteroids['Diameter_Max_KM'] = asteroids['estimated_diameter.kilometers.estimated_diameter_max']
asteroids['Miss_Distance_KM'] = asteroids['miss_distance.kilometers']
asteroids['Threat_Rank'] = asteroids['threat_score']
Step 3: Visualize Data
Create Visualizations:

Use Power BI’s visualization tools to create charts, graphs, and other visualizations from the transformed data.
For example, use scatter plots to show asteroid diameters and miss distances.

Custom 3D Plots:

To showcase advanced capabilities, generate 3D plots using Python directly in Power BI as power bi does not have its own built in . Here’s a code snippet for creating a 3D scatter plot, you can find it on the repository.
Limitations
Data Row Limitations: Power BI’s Python integration can handle up to 250,000 rows. If your dataset exceeds this, consider filtering or aggregating data.
Query Timeouts: Queries that take longer than 30 minutes may time out. Optimize your script and queries to avoid this issue.
Conclusion
By integrating Python with Power BI, you can handle API data that requires authorization headers, perform complex data transformations, and create advanced visualizations. This guide demonstrates how Python enhances Power BI’s capabilities, providing a powerful toolset for data analysis and visualization.
