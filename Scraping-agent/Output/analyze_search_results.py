# filename: analyze_search_results.py
import sys
from bs4 import BeautifulSoup

# Set the encoding to UTF-8 for the terminal
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Load the search results HTML content from the file
with open("search_results.html", "r", encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Extract relevant search results
# This will depend on the structure of the results page
results = soup.find_all("table")  # Assuming results are in a table

# Iterate through the tables and extract data
for table in results:
    rows = table.find_all("tr")
    for row in rows:
        columns = row.find_all("td")
        # Print the text content of each cell
        for column in columns:
            print(column.get_text(strip=True), end=" | ")
        print()  # New line after each row