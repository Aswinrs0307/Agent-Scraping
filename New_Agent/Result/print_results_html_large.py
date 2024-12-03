# filename: print_results_html_large.py
# Load the saved search results HTML content
with open("search_results.html", "r", encoding="utf-8") as file:
    results_html = file.read()

# Print a larger portion of the HTML content for analysis
print(results_html[:5000])  # Print the first 5000 characters for inspection