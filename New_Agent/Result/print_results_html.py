# filename: print_results_html.py
# Load the saved search results HTML content
with open("search_results.html", "r", encoding="utf-8") as file:
    results_html = file.read()

# Print a portion of the HTML content for analysis
print(results_html[:2000])  # Print the first 2000 characters for inspection