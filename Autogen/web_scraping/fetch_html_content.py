# filename: fetch_html_content.py

import requests

# URL of the webpage to scrape
url = "https://efiling.drcor.mcit.gov.cy/DrcorPublic/?cultureInfo=en-AU"

# Send a GET request to fetch the webpage content
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Write the HTML content to a file
    with open("webpage_content.html", "w", encoding="utf-8") as file:
        file.write(response.text)
    print("HTML content has been written to 'webpage_content.html'")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")