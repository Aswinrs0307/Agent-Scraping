# filename: fetch_html.py
import requests

# Step 1: Fetch the HTML content
url = "https://efiling.drcor.mcit.gov.cy/DrcorPublic/SearchForm.aspx?sc=0&cultureInfo=en-AU"
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    html_content = response.text
    # Write the HTML content to a file
    with open("output.html", "w", encoding="utf-8") as file:
        file.write(html_content)
    print("HTML content successfully written to output.html")
else:
    print(f"Failed to retrieve HTML content. Status code: {response.status_code}")