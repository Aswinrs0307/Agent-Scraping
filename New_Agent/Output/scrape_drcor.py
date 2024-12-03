# filename: scrape_drcor.py
import requests
from bs4 import BeautifulSoup

# Step 1: Fetch the HTML content
url = "https://efiling.drcor.mcit.gov.cy/DrcorPublic/SearchForm.aspx?sc=0&cultureInfo=en-AU"
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    html_content = response.text
    print("HTML content fetched successfully.")
else:
    print(f"Failed to fetch HTML content. Status code: {response.status_code}")

# Step 2: Analyze the DOM
soup = BeautifulSoup(html_content, 'html.parser')

# Identify key elements
input_fields = soup.find_all('input')
buttons = soup.find_all('button')
links = soup.find_all('a')

# Document attributes
input_attributes = [{ 'id': field.get('id'), 'name': field.get('name'), 'class': field.get('class'), 'type': field.get('type') } for field in input_fields]
button_attributes = [{ 'id': button.get('id'), 'class': button.get('class'), 'text': button.text.strip() } for button in buttons]
link_attributes = [{ 'href': link.get('href'), 'text': link.text.strip() } for link in links]

# Step 3: Save the fetched HTML content locally
with open('drcor_search_form.html', 'w', encoding='utf-8') as file:
    file.write(html_content)

print("HTML content saved to 'drcor_search_form.html'.")

# Save attributes to a separate output file
with open('attributes_output.txt', 'w', encoding='utf-8') as output_file:
    output_file.write("Input Fields:\n")
    for attr in input_attributes:
        output_file.write(f"{attr}\n")
    
    output_file.write("\nButtons:\n")
    for attr in button_attributes:
        output_file.write(f"{attr}\n")
    
    output_file.write("\nLinks:\n")
    for attr in link_attributes:
        output_file.write(f"{attr}\n")

print("Attributes saved to 'attributes_output.txt'.")