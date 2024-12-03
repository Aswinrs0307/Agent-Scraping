# filename: save_results.py
from bs4 import BeautifulSoup

# Load the updated HTML content from the saved file
with open("updated_search_results.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML content
soup = BeautifulSoup(html_content, "html.parser")

# Identify the relevant elements in the search results
results = soup.find_all("tr")  # Assuming results are in table rows

# Prepare to save the results to a text file
with open("search_results.txt", "w", encoding="utf-8") as output_file:
    for result in results:
        columns = result.find_all("td")  # Assuming data is in table cells
        if columns:
            data = [col.get_text(strip=True) for col in columns]
            # Write the data to the text file
            output_file.write(" | ".join(data) + "\n")

print("Search results saved to search_results.txt.")