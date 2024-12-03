# filename: extract_td_links.py
from bs4 import BeautifulSoup

# Load the saved search results HTML content
with open("search_results.html", "r", encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, "html.parser")

# Find all <td> elements
td_elements = soup.find_all("td")

# Extract links from <td> elements
td_links = []
for td in td_elements:
    links = td.find_all("a")  # Find all <a> tags within the <td>
    for link in links:
        href = link.get("href")
        text = link.get_text(strip=True)
        if href:  # Only consider valid links
            td_links.append({"text": text, "link": href})

# Output the extracted links from <td> elements
print("Extracted Links from <td> Tags:")
for link_info in td_links:
    print(link_info)