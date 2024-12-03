# filename: follow_links.py
from bs4 import BeautifulSoup
import requests

# Load the search results HTML content from the file
with open("search_results.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, "html.parser")

# Step 6.1: Locate the relevant link associated with the extracted result
# Assuming the relevant link is in the same row as the found text
results = soup.find_all("td")  # Get all table cells

# Step 6.2: Check for links in the same row as the company name
for td in results:
    if "BANK OF CYPRUS PUBLIC COMPANY LIMITED" in td.get_text():
        # Find the link in the same row
        link = td.find("a")
        if link and link.get("href"):
            detail_url = link["href"]
            print(f"Found link to details: {detail_url}")
            
            # Fetch the details from the link
            response = requests.get(detail_url)
            if response.status_code == 200:
                detail_html = response.text
                with open("company_details.html", "w", encoding="utf-8") as detail_file:
                    detail_file.write(detail_html)
                print("Company details successfully written to company_details.html")
            else:
                print(f"Failed to retrieve details. Status code: {response.status_code}")