# filename: analyze_dom.py
import sys
from bs4 import BeautifulSoup

# Set the encoding to UTF-8 for the terminal
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

# Load the HTML content from the file
with open("page_content.html", "r", encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

# Extract input fields
input_fields = soup.find_all("input")
for input_field in input_fields:
    print("Input Field:")
    print("Type:", input_field.get("type"))
    print("ID:", input_field.get("id"))
    print("Name:", input_field.get("name"))
    print("Class:", input_field.get("class"))
    print("Placeholder:", input_field.get("placeholder"))
    print()

# Extract buttons
buttons = soup.find_all("button")
for button in buttons:
    print("Button:")
    print("ID:", button.get("id"))
    print("Class:", button.get("class"))
    print("Text:", button.get_text())
    print()

# Extract links
links = soup.find_all("a")
for link in links:
    print("Link:")
    print("Href:", link.get("href"))
    print("Text:", link.get_text())
    print()

# Extract tables
tables = soup.find_all("table")
for table in tables:
    print("Table found with ID:", table.get("id"))