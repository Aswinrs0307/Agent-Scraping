# filename: debug_search_results.py

from bs4 import BeautifulSoup

# Read the HTML content from the saved file
with open('search_results.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

# Find the search results table
results_table = soup.find('table', {'id': 'ctl00_MainContent_gvResults'})

# Debug: Print the text content of each row in the search results table
if results_table:
    for row in results_table.find_all('tr'):
        columns = row.find_all('td')
        row_text = [col.text.strip() for col in columns]
        print(row_text)
else:
    print("No results table found.")