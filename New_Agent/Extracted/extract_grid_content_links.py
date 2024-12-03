# filename: extract_grid_content_links.py
from bs4 import BeautifulSoup

# Load the saved search results HTML content
with open("search_results.html", "r", encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, "html.parser")

# Find all elements with class 'gridContent'
grid_content_elements = soup.find_all(class_="gridContent")

# Extract links from elements with class 'gridContent'
grid_content_links = []
for element in grid_content_elements:
    links = element.find_all("a")  # Find all <a> tags within the element
    for link in links:
        href = link.get("href")
        text = link.get_text(strip=True)
        if href:  # Only consider valid links
            grid_content_links.append({"text": text, "link": href})

# Output the extracted links from elements with class 'gridContent'
print("Extracted Links from 'gridContent' Class:")
for link_info in grid_content_links:
    print(link_info)