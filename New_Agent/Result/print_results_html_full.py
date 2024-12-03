# filename: print_results_html_full.py
from sys import stdout

# Load the saved search results HTML content
with open("search_results.html", "r", encoding="utf-8") as file:
    results_html = file.read()

# Print the entire HTML content for analysis
def safe_print(data):
    print(data.encode(stdout.encoding, errors='replace').decode(stdout.encoding))

safe_print(results_html)  # Print the entire HTML content for inspection