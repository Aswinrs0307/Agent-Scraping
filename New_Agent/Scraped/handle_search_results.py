# filename: handle_search_results.py
import sys
from bs4 import BeautifulSoup

# Set the encoding for the output
sys.stdout.reconfigure(encoding='utf-8')

# Load the search results HTML file
with open("search_results.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, "html.parser")

# Find relevant elements in the search results
# This will depend on the structure of the results page
# For example, we might look for table rows or specific links

# Example: Find all links in the search results
result_links = soup.find_all("a")
result_info = [{"href": link.get("href"), "text": link.text.strip()} for link in result_links if link.get("href")]

# Print the extracted result links
print("Result Links:")
for info in result_info:
    print(info)