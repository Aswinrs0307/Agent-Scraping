# filename: analyze_html.py
from bs4 import BeautifulSoup

# Step 2: Load the HTML content from the file
with open("output.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, "html.parser")

# Step 2.1: Identify all text input fields related to search functionality
input_fields = soup.find_all("input", type="text")

# Step 2.2: Document the attributes of the input fields
input_attributes = []
for input_field in input_fields:
    attributes = {
        "id": input_field.get("id"),
        "name": input_field.get("name"),
        "class": input_field.get("class"),
        "placeholder": input_field.get("placeholder")
    }
    input_attributes.append(attributes)

# Step 2.3: Save input fields and attributes for re-use
print("Identified input fields and their attributes:")
for attributes in input_attributes:
    print(attributes)