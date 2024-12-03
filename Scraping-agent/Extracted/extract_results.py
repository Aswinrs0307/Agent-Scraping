# filename: extract_results.py
from bs4 import BeautifulSoup

# Load the saved search results HTML content
with open("search_results.html", "r", encoding="utf-8") as file:
    search_results_html = file.read()

# Parse the HTML content
soup = BeautifulSoup(search_results_html, "html.parser")

# Identify and extract relevant search results
results = soup.find_all("a")  # Adjust this based on the actual structure of the results

# Document the extracted results
extracted_results = []
for result in results:
    details = {
        "text": result.text,
        "href": result.get("href"),
        "id": result.get("id"),
        "class": result.get("class"),
    }
    extracted_results.append(details)

# Save the extracted results to a file
with open("extracted_results.txt", "w", encoding="utf-8") as output_file:
    for detail in extracted_results:
        output_file.write(f"Text: {detail['text']}, Href: {detail['href']}, ID: {detail['id']}, Class: {detail['class']}\n")

print("Extracted results saved to extracted_results.txt.")