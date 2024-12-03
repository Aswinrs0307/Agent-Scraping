# filename: save_search_results_inspection.py
# Load the saved search results HTML content
with open("search_results.html", "r", encoding="utf-8") as file:
    search_results_html = file.read()

# Save the HTML content to a new file for inspection
with open("search_results_inspection.html", "w", encoding="utf-8") as output_file:
    output_file.write(search_results_html)

print("Search results saved to search_results_inspection.html for inspection.")