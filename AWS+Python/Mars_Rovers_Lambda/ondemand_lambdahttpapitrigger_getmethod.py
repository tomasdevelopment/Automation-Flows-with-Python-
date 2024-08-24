import requests

# API Gateway URL
url = "https://123.execute-api.sa-east-1.amazonaws.com/default/Nasa_Rovers_Lambda"

# Make the GET request
response = requests.get(url)

# Print the response
print(response.status_code)
print(response.json())


#This will trigger on demand, for real operational purposes add api key to your gateways always.
