# filename: extract_search_fields.py
from bs4 import BeautifulSoup

# Load the saved HTML content
with open("page_content.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, "html.parser")

# Find all relevant input fields for search functionality
search_fields = []
input_fields = soup.find_all("input")

for input_field in input_fields:
    if input_field.get("type") == "text" or "search" in input_field.get("type", "").lower():
        search_fields.append({
            "id": input_field.get("id"),
            "name": input_field.get("name"),
            "class": input_field.get("class"),
            "placeholder": input_field.get("placeholder"),
        })

# Save the search fields to a file for reuse
with open("search_fields.json", "w", encoding="utf-8") as json_file:
    import json
    json.dump(search_fields, json_file, ensure_ascii=False, indent=4)

print("Search fields extracted and saved to search_fields.json.")