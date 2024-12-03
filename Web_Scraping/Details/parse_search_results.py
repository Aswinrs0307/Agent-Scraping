# filename: parse_search_results.py

from bs4 import BeautifulSoup

# Read the HTML content from the saved file
with open('search_results.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find the search results table
results_table = soup.find('table', {'id': 'ctl00_MainContent_gvResults'})

# Extract the details of the company
company_details = ""
if results_table:
    for row in results_table.find_all('tr')[1:]:  # Skip the header row
        columns = row.find_all('td')
        if columns and columns[0].text.strip() == "BANK OF CYPRUS PUBLIC COMPANY LIMITED":
            company_details = "\n".join([col.text.strip() for col in columns])
            break

# Save the details to a text file
with open('bank_of_cyprus_details.txt', 'w', encoding='utf-8') as file:
    file.write(company_details)

print("Details of BANK OF CYPRUS PUBLIC COMPANY LIMITED have been saved to 'bank_of_cyprus_details.txt'.")