# filename: find_search_trigger.py
from bs4 import BeautifulSoup

# Load the HTML content from the file
with open("output.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, "html.parser")

# Step 3.1: Locate the search trigger element
# Look for <button>, <input type="submit">, or <a> tags
search_triggers = soup.find_all(["button", "input", "a"])

# Step 3.2: Document the attributes of the search triggers
trigger_attributes = []
for trigger in search_triggers:
    if trigger.name == "button" or (trigger.name == "input" and trigger.get("type") == "submit"):
        attributes = {
            "id": trigger.get("id"),
            "name": trigger.get("name"),
            "class": trigger.get("class"),
            "onclick": trigger.get("onclick"),
            "type": trigger.get("type")
        }
        trigger_attributes.append(attributes)
    elif trigger.name == "a":
        attributes = {
            "id": trigger.get("id"),
            "href": trigger.get("href"),
            "onclick": trigger.get("onclick"),
            "class": trigger.get("class")
        }
        trigger_attributes.append(attributes)

# Step 3.4: Print the identified triggers and their attributes
print("Identified search triggers and their attributes:")
for attributes in trigger_attributes:
    print(attributes)