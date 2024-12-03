# filename: web_scraping_task.py

import requests
from bs4 import BeautifulSoup
import json

# Step 1: Send a GET request to the provided URL
url = "{url}"  # Replace {url} with the actual URL
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Step 2: Locate the search form and fill in the details
search_form = soup.find('form', {'id': 'searchForm'})  # Adjust the form ID or class if necessary
search_url = search_form['action']  # Get the form action URL

# Step 3: Fill in the search form with the name "jack"
search_data = {
    'name': 'jack',  # Adjust the input name attribute if necessary
    'reg_no': ''  # Leave the registration number empty
}

# Step 4: Submit the form and navigate to the search results page
search_response = requests.post(search_url, data=search_data)
search_soup = BeautifulSoup(search_response.content, 'html.parser')

# Step 5: Extract the link of the first search result
first_result_link = search_soup.find('a', {'class': 'result-link'})['href']  # Adjust the class or tag if necessary

# Step 6: Navigate to the details page of the first search result
details_response = requests.get(first_result_link)
details_soup = BeautifulSoup(details_response.content, 'html.parser')

# Step 7: Extract the required information from the table on the details page
table = details_soup.find('table', {'id': 'detailsTable'})  # Adjust the table ID or class if necessary
rows = table.find_all('tr')

data = {}
for row in rows:
    cols = row.find_all('td')
    if len(cols) == 2:
        key = cols[0].text.strip()
        value = cols[1].text.strip()
        if key in ["Name", "Reg. Number", "Type", "Name Status", "Organisation Status"]:
            data[key] = value

# Step 8: Format the extracted information in JSON format and print it
print(json.dumps(data, indent=4))