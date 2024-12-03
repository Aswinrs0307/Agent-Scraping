# filename: analyze_results.py
from bs4 import BeautifulSoup

# Load the saved search results HTML content
with open("search_results.html", "r", encoding="utf-8") as file:
    results_html = file.read()

# Parse the HTML content
soup = BeautifulSoup(results_html, "html.parser")

# Find all relevant result elements (adjust the selector based on the actual structure)
# For demonstration, we will look for <a> tags within a specific results container
results_container = soup.find("div", class_="results-container")  # Adjust class name as needed
result_links = results_container.find_all("a") if results_container else []

# Extract relevant information from the results
extracted_results = []

for link in result_links:
    extracted_results.append({
        "href": link.get("href"),
        "text": link.text.strip()
    })

# Output the extracted results
print("Extracted Search Results:")
for result in extracted_results:
    print(result)