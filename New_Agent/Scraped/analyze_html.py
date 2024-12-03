# filename: analyze_html.py
import sys
from bs4 import BeautifulSoup

# Load the HTML content from the saved file
with open("fetched_html.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, "html.parser")

# Identify input fields
input_fields = soup.find_all("input")
input_info = []

for input_field in input_fields:
    attributes = {
        "type": input_field.get("type"),
        "id": input_field.get("id"),
        "name": input_field.get("name"),
        "class": input_field.get("class"),
        "placeholder": input_field.get("placeholder"),
    }
    input_info.append(attributes)

# Identify buttons
buttons = soup.find_all("button")
button_info = []

for button in buttons:
    attributes = {
        "id": button.get("id"),
        "class": button.get("class"),
        "type": button.get("type"),
        "onclick": button.get("onclick"),
    }
    button_info.append(attributes)

# Identify links
links = soup.find_all("a")
link_info = []

for link in links:
    attributes = {
        "href": link.get("href"),
        "id": link.get("id"),
        "class": link.get("class"),
        "text": link.get_text(strip=True),
    }
    link_info.append(attributes)

# Output the identified elements
def safe_print(data):
    print(data.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding))

safe_print("Input Fields:")
for info in input_info:
    safe_print(str(info))

safe_print("\nButtons:")
for info in button_info:
    safe_print(str(info))

safe_print("\nLinks:")
for info in link_info:
    safe_print(str(info))