# filename: inspect_search_results.py
# Load the saved search results HTML content
with open("search_results.html", "r", encoding="utf-8") as file:
    search_results_html = file.read()

# Print the HTML content to inspect its structure
print(search_results_html)