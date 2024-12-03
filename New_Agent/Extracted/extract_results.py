# filename: extract_results.py
from bs4 import BeautifulSoup

# Load the saved search results HTML content
with open("search_results.html", "r", encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, "html.parser")

# Find all relevant elements in the search results
# This will depend on the structure of the search results page
# For example, if results are in a table or specific divs, adjust the selectors accordingly
results = soup.find_all("a")  # Adjust this to target the correct elements

# Extract and print relevant information
extracted_links = []
for result in results:
    link = result.get("href")
    text = result.get_text(strip=True)
    if link:  # Only consider valid links
        extracted_links.append({"text": text, "link": link})

# Output the extracted links
print("Extracted Links:")
for link_info in extracted_links:
    print(link_info)