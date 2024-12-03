# filename: debug_full_html.py

# Read the HTML content from the saved file
with open('search_results.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Save the full HTML content to a file for inspection
with open('full_html_debug.html', 'w', encoding='utf-8') as file:
    file.write(html_content)

print("The full HTML content has been saved to 'full_html_debug.html'.")