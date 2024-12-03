# filename: scrape_jack_details.py

import requests
from bs4 import BeautifulSoup

# URL of the website to scrape
url = "https://efiling.drcor.mcit.gov.cy/DrcorPublic/?cultureInfo=en-AU"

# Send a GET request to the website
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all occurrences of the name "Jack" and retrieve details
    details = []
    for person in soup.find_all(text="Jack"):
        parent = person.find_parent()
        details.append(parent.get_text(strip=True))
    
    # Save the details to a text file
    with open("jack_details.txt", "w") as file:
        for detail in details:
            file.write(detail + "\n")
    
    print("Details of the person named Jack have been saved to jack_details.txt")
else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)