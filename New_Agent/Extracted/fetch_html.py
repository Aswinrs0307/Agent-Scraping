# filename: fetch_html.py
import requests

# URL to fetch
url = "https://efiling.drcor.mcit.gov.cy/DrcorPublic/SearchForm.aspx?sc=0&cultureInfo=en-AU"

# Fetch the HTML content
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Save the HTML content to a file
    with open("fetched_page.html", "w", encoding='utf-8') as file:
        file.write(response.text)
    print("HTML content fetched and saved to 'fetched_page.html'.")
else:
    print(f"Failed to fetch the page. Status code: {response.status_code}")