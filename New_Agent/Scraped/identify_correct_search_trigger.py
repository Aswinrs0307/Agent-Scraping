# filename: identify_correct_search_trigger.py
import sys
from bs4 import BeautifulSoup

# Set the encoding for the output
sys.stdout.reconfigure(encoding='utf-8')

# Load the saved HTML file
with open("fetched_page.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, "html.parser")

# Find the correct search trigger element (the link that triggers the search)
search_trigger = soup.find("a", text="Go")

# Document the attributes of the search trigger
if search_trigger:
    trigger_info = {
        "href": search_trigger.get("href"),
        "text": search_trigger.text.strip(),
        "id": search_trigger.get("id"),
        "class": search_trigger.get("class")
    }
    print("Search Trigger:")
    print(trigger_info)
else:
    print("Search trigger not found.")