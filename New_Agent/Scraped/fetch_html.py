# filename: fetch_html.py
import requests

# URL to fetch
url = "https://efiling.drcor.mcit.gov.cy/DrcorPublic/SearchForm.aspx?sc=0&cultureInfo=en-AU"

# Fetch the HTML content
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Save the HTML content to a file
    with open("fetched_html.html", "w", encoding="utf-8") as file:
        file.write(response.text)
    print("HTML content fetched and saved successfully.")
else:
    print(f"Failed to fetch HTML content. Status code: {response.status_code}")