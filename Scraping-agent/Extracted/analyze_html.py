# filename: analyze_html.py
from bs4 import BeautifulSoup

# Load the saved HTML content
with open("page_content.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, "html.parser")

# Extract input fields
input_fields = soup.find_all("input")
input_details = []

for input_field in input_fields:
    details = {
        "type": input_field.get("type"),
        "id": input_field.get("id"),
        "name": input_field.get("name"),
        "class": input_field.get("class"),
        "placeholder": input_field.get("placeholder"),
    }
    input_details.append(details)

# Extract buttons
buttons = soup.find_all("button")
button_details = []

for button in buttons:
    details = {
        "id": button.get("id"),
        "class": button.get("class"),
        "onclick": button.get("onclick"),
    }
    button_details.append(details)

# Extract links
links = soup.find_all("a")
link_details = []

for link in links:
    details = {
        "href": link.get("href"),
        "id": link.get("id"),
        "class": link.get("class"),
    }
    link_details.append(details)

# Print the extracted details
print("Input Fields:")
for detail in input_details:
    print(detail)

print("\nButtons:")
for detail in button_details:
    print(detail)

print("\nLinks:")
for detail in link_details:
    print(detail)