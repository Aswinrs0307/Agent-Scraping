# filename: identify_search_trigger.py
from bs4 import BeautifulSoup

# Load the saved HTML content
with open("page_content.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, "html.parser")

# Find the search trigger element
search_triggers = []

# Check for button elements
buttons = soup.find_all("button")
for button in buttons:
    if "search" in button.text.lower() or "submit" in button.text.lower():
        search_triggers.append({
            "id": button.get("id"),
            "class": button.get("class"),
            "text": button.text.strip(),
        })

# Check for input type submit
submit_inputs = soup.find_all("input", type="submit")
for submit_input in submit_inputs:
    search_triggers.append({
        "id": submit_input.get("id"),
        "class": submit_input.get("class"),
        "text": submit_input.get("value"),
    })

# Check for anchor tags that might act as triggers
links = soup.find_all("a")
for link in links:
    if "search" in link.text.lower():
        search_triggers.append({
            "href": link.get("href"),
            "text": link.text.strip(),
        })

# Save the search triggers to a file for reuse
with open("search_triggers.json", "w", encoding="utf-8") as json_file:
    import json
    json.dump(search_triggers, json_file, ensure_ascii=False, indent=4)

print("Search triggers identified and saved to search_triggers.json.")