# filename: extract_detail_pages.py
import requests
from bs4 import BeautifulSoup

# Load the identified links from the output file
with open('blackjack_links_output.txt', 'r', encoding='utf-8') as file:
    links = file.readlines()

# Prepare to store details
details = []

# Step 1: Fetch HTML content for each link
for line in links[1:]:  # Skip the header line
    link_info = eval(line.strip())  # Convert string representation of dict back to dict
    href = link_info['href']
    
    # Construct full URL if necessary (assuming href is relative)
    if href.startswith('/'):
        href = f"https://efiling.drcor.mcit.gov.cy{href}"
    
    response = requests.get(href)
    
    # Step 2: Check if the request was successful
    if response.status_code == 200:
        print(f"Fetched details from: {href}")
        detail_soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract relevant details (modify as needed based on the page structure)
        detail_content = detail_soup.get_text(separator="\n").strip()
        details.append({'url': href, 'content': detail_content})
        
        # Save the detail page HTML
        with open(f'detail_page_{len(details)}.html', 'w', encoding='utf-8') as detail_file:
            detail_file.write(response.text)
    else:
        print(f"Failed to fetch details from {href}. Status code: {response.status_code}")

# Save extracted details to a file
with open('extracted_details.txt', 'w', encoding='utf-8') as output_file:
    for detail in details:
        output_file.write(f"URL: {detail['url']}\nContent:\n{detail['content']}\n\n")

print("Extracted details saved to 'extracted_details.txt'.")