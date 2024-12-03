# filename: extract_search_results.py
from bs4 import BeautifulSoup

# Load the saved search results HTML content
with open("search_results.html", "r", encoding="utf-8") as file:
    results_html = file.read()

# Parse the HTML content
soup = BeautifulSoup(results_html, "html.parser")

# Find the results table
results_table = soup.find("table", id="ctl00_cphMyMasterCentral_GridView1")
extracted_results = []

if results_table:
    rows = results_table.find_all("tr")[1:]  # Skip the header row
    for row in rows:
        columns = row.find_all("td")
        if columns:
            result = {
                "Name": columns[1].text.strip(),
                "Reg. Number": columns[3].text.strip(),
                "Type": columns[4].text.strip(),
                "Name Status": columns[5].text.strip(),
                "Organisation Status": columns[6].text.strip(),
            }
            extracted_results.append(result)

# Output the extracted results
print("Extracted Search Results:")
for result in extracted_results:
    print(result)