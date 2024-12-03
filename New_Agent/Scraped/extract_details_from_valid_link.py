# filename: extract_details_from_valid_link.py
import sys
import requests
from bs4 import BeautifulSoup

# Set the encoding for the output
sys.stdout.reconfigure(encoding='utf-8')

# Valid link to navigate to
valid_link = "https://eforms.eservices.cyprus.gov.cy/MCIT/RCOR/OrganisationFileSearch"

# Make a GET request to the valid link
response = requests.get(valid_link)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract relevant information (this will depend on the structure of the page)
    # For example, we might look for specific tables, headings, or other elements
    # Here, we will just print the title of the page as an example
    page_title = soup.title.string if soup.title else "No title found"
    print(f"Page Title: {page_title}")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")