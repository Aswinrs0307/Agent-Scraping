# filename: extract_search_results.py
from bs4 import BeautifulSoup

# Load the search results HTML content from the file
with open("search_results.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, "html.parser")

# Step 6.1: Locate and document relevant text or elements related to the search query
# This will depend on the structure of the search results page
results = soup.find_all(text=True)  # Get all text elements

# Step 6.2: Document the results
extracted_results = []
for result in results:
    if "BANK OF CYPRUS PUBLIC COMPANY LIMITED" in result:
        parent = result.parent  # Get the parent element for context
        extracted_results.append({
            "text": result.strip(),
            "parent_tag": parent.name,
            "parent_attributes": parent.attrs
        })

# Step 6.3: Print the extracted results
print("Extracted search results related to BANK OF CYPRUS PUBLIC COMPANY LIMITED:")
for result in extracted_results:
    print(result)