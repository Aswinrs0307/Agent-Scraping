# filename: analyze_html.py
from bs4 import BeautifulSoup
import sys

# Load the saved HTML content
with open("fetched_page.html", "r", encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, "html.parser")

# Find all input fields
input_fields = soup.find_all("input")
input_info = []
for input_field in input_fields:
    input_info.append({
        "type": input_field.get("type"),
        "id": input_field.get("id"),
        "name": input_field.get("name"),
        "class": input_field.get("class"),
        "placeholder": input_field.get("placeholder")
    })

# Find all buttons
buttons = soup.find_all("button")
button_info = []
for button in buttons:
    button_info.append({
        "id": button.get("id"),
        "class": button.get("class"),
        "text": button.get_text(strip=True)
    })

# Find all links
links = soup.find_all("a")
link_info = []
for link in links:
    link_info.append({
        "href": link.get("href"),
        "text": link.get_text(strip=True)
    })

# Output the collected information
sys.stdout.reconfigure(encoding='utf-8')  # Ensure proper encoding for output

print("Input Fields:")
for info in input_info:
    print(info)

print("\nButtons:")
for info in button_info:
    print(info)

print("\nLinks:")
for info in link_info:
    print(info)