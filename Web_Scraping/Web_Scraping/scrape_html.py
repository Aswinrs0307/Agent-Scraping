# filename: scrape_html.py
import requests

url = "https://efiling.drcor.mcit.gov.cy/DrcorPublic/SearchForm.aspx?sc=0&cultureInfo=en-AU"
response = requests.get(url)

# Print the HTML content of the page with utf-8 encoding
print(response.text.encode('utf-8', errors='ignore').decode('utf-8'))