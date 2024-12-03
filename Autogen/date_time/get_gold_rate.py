# filename: get_gold_rate.py
import requests

# Your API key (replace 'YOUR_API_KEY' with your actual API key)
api_key = 'YOUR_API_KEY'

# URL of the API to get gold rate
url = "https://www.goldapi.io/api/XAU/INR"

# Headers for the API request
headers = {
    'x-access-token': api_key,
    'Content-Type': 'application/json'
}

# Send a GET request to the API
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    gold_rate = data['price']
    print(f"Today's gold rate in Tamil Nadu: {gold_rate} INR per gram")
else:
    print("Failed to retrieve gold rate. Please check your API key and try again.")