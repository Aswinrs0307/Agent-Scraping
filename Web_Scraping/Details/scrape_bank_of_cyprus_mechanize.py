# filename: scrape_bank_of_cyprus_mechanize.py

import mechanize
from bs4 import BeautifulSoup

# URL of the search form
url = "https://efiling.drcor.mcit.gov.cy/DrcorPublic/SearchForm.aspx?sc=0&cultureInfo=en-AU"

# Create a browser object
br = mechanize.Browser()
br.set_handle_robots(False)  # Ignore robots.txt
br.open(url)

# Select the search form
br.select_form(nr=0)

# Fill in the search form
br["ctl00$MainContent$txtName"] = "BANK OF CYPRUS PUBLIC COMPANY LIMITED"

# Submit the form
response = br.submit()

# Parse the response
soup = BeautifulSoup(response.read(), 'html.parser')

# Find the search results table
results_table = soup.find('table', {'id': 'ctl00_MainContent_gvResults'})

# Extract the details of the company
company_details = ""
if results_table:
    for row in results_table.find_all('tr')[1:]:  # Skip the header row
        columns = row.find_all('td')
        if columns[0].text.strip() == "BANK OF CYPRUS PUBLIC COMPANY LIMITED":
            company_details = "\n".join([col.text.strip() for col in columns])
            break

# Save the details to a text file
with open('bank_of_cyprus_details.txt', 'w') as file:
    file.write(company_details)

print("Details of BANK OF CYPRUS PUBLIC COMPANY LIMITED have been saved to 'bank_of_cyprus_details.txt'.")