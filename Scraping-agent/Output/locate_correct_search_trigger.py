# filename: locate_correct_search_trigger.py
from bs4 import BeautifulSoup

# Load the HTML content from the file
with open("page_content.html", "r", encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Locate the correct search trigger element
search_trigger = soup.find("a", href=lambda href: href and "javascript:__doPostBack" in href and "lbtnSearch" in href)

if search_trigger:
    print("Search Trigger Found:")
    print("ID:", search_trigger.get("id"))
    print("Href:", search_trigger.get("href"))
    print("Text:", search_trigger.get_text())
else:
    print("Search trigger not found.")