import requests
import json
from pprint import pprint

# Function to fetch rover manifest
def get_rover_manifest(rover_name):
    # API endpoint URL
    url = f"https://api.nasa.gov/mars-photos/api/v1/manifests/{rover_name}"

    # Parameters for the API request
    params = {
        "api_key": "DEMO_KEY"  # Replace with your actual API key
    }

    try:
        # Send GET request to the API
        response = requests.get(url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            return data['photo_manifest']
        else:
            print(f"Error: Received status code {response.status_code}")
            print(response.text)
            return None

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Function to display rover manifest information
def display_rover_manifest(manifest):
    print(f"Rover Name: {manifest['name']}")
    print(f"Landing Date: {manifest['landing_date']}")
    print(f"Launch Date: {manifest['launch_date']}")
    print(f"Status: {manifest['status']}")
    print(f"Max Sol: {manifest['max_sol']}")
    print(f"Max Date: {manifest['max_date']}")
    print(f"Total Photos: {manifest['total_photos']}")

    print("\nPhotos by Sol:")
    for photo_data in manifest['photos'][:5]:  # Display info for first 5 sols
        print(f"  Sol {photo_data['sol']}:")
        print(f"    Total Photos: {photo_data['total_photos']}")
        print(f"    Cameras: {', '.join(photo_data['cameras'])}")

    if len(manifest['photos']) > 5:
        print("  ...")  # Indicate there are more sols not shown

# Main execution
if __name__ == "__main__":
    rover_name = input("Enter the name of the Mars Rover (e.g., Curiosity, Opportunity, Spirit): ")
    manifest = get_rover_manifest(rover_name)
    
    if manifest:
        display_rover_manifest(manifest)
    else:
        print(f"Failed to retrieve manifest for {rover_name}")
