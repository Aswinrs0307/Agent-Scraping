# filename: scrape_bank_of_cyprus_full_html.py

import requests
from bs4 import BeautifulSoup

# URL of the search form
url = "https://efiling.drcor.mcit.gov.cy/DrcorPublic/SearchForm.aspx?sc=0&cultureInfo=en-AU"

# Create a session to persist the cookies
session = requests.Session()

# Perform a GET request to get the search form
response = session.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Extract the viewstate and eventvalidation values required for the form submission
viewstate = soup.find('input', {'id': '__VIEWSTATE'})['value']
eventvalidation = soup.find('input', {'id': '__EVENTVALIDATION'})['value']

# Data for the POST request to perform the search
data = {
    '__VIEWSTATE': viewstate,
    '__EVENTVALIDATION': eventvalidation,
    'ctl00$MainContent$txtName': 'BANK OF CYPRUS PUBLIC COMPANY LIMITED',
    'ctl00$MainContent$btnSearch': 'Search'
}

# Perform the POST request to search for the company
response = session.post(url, data=data)
soup = BeautifulSoup(response.content, 'html.parser')

# Save the entire HTML content to a file for inspection
with open('search_results_full.html', 'w', encoding='utf-8') as file:
    file.write(soup.prettify())

print("The full HTML content of the search results page has been saved to 'search_results_full.html'.")