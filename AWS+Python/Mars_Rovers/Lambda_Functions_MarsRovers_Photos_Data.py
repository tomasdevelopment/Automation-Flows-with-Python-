import requests
import pandas as pd

# Function to fetch rover manifest
def get_rover_manifest(rover_name):
    url = f"https://api.nasa.gov/mars-photos/api/v1/manifests/{rover_name}"
    params = {
        "api_key": "yourapikey"
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data['photo_manifest']
        else:
            print(f"Error fetching data for {rover_name}: Status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching data for {rover_name}: {e}")
        return None

# Function to process rover data
def process_rover_data(manifest):
    return {
        "Name": manifest['name'],
        "Landing Date": manifest['landing_date'],
        "Launch Date": manifest['launch_date'],
        "Status": manifest['status'],
        "Max Sol": manifest['max_sol'],
        "Max Date": manifest['max_date'],
        "Total Photos": manifest['total_photos'],
        "Latest Sol Photos": manifest['photos'][-1]['total_photos'],
        "Latest Sol Cameras": ", ".join(manifest['photos'][-1]['cameras'])
    }

# Main execution
if __name__ == "__main__":
    rovers = ["Curiosity", "Opportunity", "Spirit"]
    rover_data = []

    for rover in rovers:
        manifest = get_rover_manifest(rover)
        if manifest:
            rover_data.append(process_rover_data(manifest))

    if rover_data:
        # Create pandas DataFrame
        df = pd.DataFrame(rover_data)
        
        # Set 'Name' as the index
        df.set_index('Name', inplace=True)
        
        # Display the DataFrame
        print(df)
        
        # Optional: Display DataFrame info
        print("\nDataFrame Info:")
        print(df.info())
        
        # Optional: Save to CSV
        df.to_csv('mars_rover_manifests.csv')
        print("\nDataFrame saved to 'mars_rover_manifests.csv'")
    else:
        print("Failed to retrieve data for any rovers.")
