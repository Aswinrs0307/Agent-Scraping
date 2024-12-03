# filename: scrape_bank_of_cyprus_debug_rows.py

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

# Find the search results table
results_table = soup.find('table', {'id': 'ctl00_MainContent_gvResults'})

# Debug: Print the rows of the search results table
if results_table:
    for row in results_table.find_all('tr'):
        print(row.prettify())

# Extract the details of the company
company_details = ""
if results_table:
    for row in results_table.find_all('tr')[1:]:  # Skip the header row
        columns = row.find_all('td')
        if columns[0].text.strip() == "BANK OF CYPRUS PUBLIC COMPANY LIMITED":
            company_details = "\n".join([col.text.strip() for col in columns])
            break

# Save the details to a text file
with open('bank_of_cyprus_details.txt', 'w', encoding='utf-8') as file:
    file.write(company_details)

print("Details of BANK OF CYPRUS PUBLIC COMPANY LIMITED have been saved to 'bank_of_cyprus_details.txt'.")