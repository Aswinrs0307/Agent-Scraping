# filename: analyze_results.py
import sys
from bs4 import BeautifulSoup

# Load the updated HTML content from the saved file
with open("updated_search_results.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, "html.parser")

# Identify the relevant elements in the search results
# This will depend on the structure of the HTML. For example, if results are in a table:
results = soup.find_all("tr")  # Assuming results are in table rows

# Extract and print the relevant information
def safe_print(data):
    print(" | ".join(data).encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding))

for result in results:
    columns = result.find_all("td")  # Assuming data is in table cells
    if columns:
        data = [col.get_text(strip=True) for col in columns]
        safe_print(data)

# You can also save the extracted data to a file or process it further as needed.