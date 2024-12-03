# filename: simulate_search.py
from bs4 import BeautifulSoup

# Load the HTML content from the saved file
with open("fetched_html.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, "html.parser")

# Identify the search button using the onclick attribute
search_button = soup.find("a", {"id": "ctl00_cphMyMasterCentral_ucSearch_lbtnSearch"})

# Output the search button attributes
if search_button:
    search_button_info = {
        "id": search_button.get("id"),
        "class": search_button.get("class"),
        "onclick": search_button.get("onclick"),
        "text": search_button.get_text(strip=True),
    }
    print("Search Button Info:")
    print(search_button_info)
else:
    print("Search button not found. Here are all links:")
    all_links = soup.find_all("a")
    for link in all_links:
        print({
            "href": link.get("href"),
            "id": link.get("id"),
            "class": link.get("class"),
            "text": link.get_text(strip=True),
        })

# Prepare to simulate user input
search_query = {
    "name": "BLACK JACK SPORTS BETTING",
    "number": ""  # Assuming we are only searching by name
}

print("\nSimulated User Input:")
print(f"Name: {search_query['name']}")
print(f"Number: {search_query['number']}")