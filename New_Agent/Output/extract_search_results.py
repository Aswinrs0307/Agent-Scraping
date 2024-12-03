# filename: extract_search_results.py
from bs4 import BeautifulSoup

# Load the saved search results HTML content
with open('search_results.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Step 1: Analyze the results page
soup = BeautifulSoup(html_content, 'html.parser')

# Identify result links (assuming they are in <a> tags)
result_links = soup.find_all('a')

# Filter links related to "BLACK JACK SPORTS BETTING"
blackjack_links = []
for link in result_links:
    if "BLACK JACK SPORTS BETTING" in link.text:
        blackjack_links.append({'href': link.get('href'), 'text': link.text.strip()})

# Save identified links to a file
with open('blackjack_links_output.txt', 'w', encoding='utf-8') as output_file:
    output_file.write("Links related to 'BLACK JACK SPORTS BETTING':\n")
    for link in blackjack_links:
        output_file.write(f"{link}\n")

print("Identified links saved to 'blackjack_links_output.txt'.")