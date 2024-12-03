# filename: simulate_search.py
import requests
from bs4 import BeautifulSoup

# Load the saved HTML content to retrieve input field names
with open('drcor_search_form.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, 'html.parser')

# Identify the search input fields and button
search_input_fields = soup.find_all('input', {'type': 'text'})
search_button = soup.find('input', {'type': 'submit'})  # Assuming the search button is of type submit

# Prepare the search parameters
search_params = {}
for field in search_input_fields:
    field_name = field.get('name')
    if field_name:
        search_params[field_name] = "BLACK JACK SPORTS BETTING"  # Entering the search query

# URL to submit the search form (this may need to be adjusted based on the form action)
search_url = "https://efiling.drcor.mcit.gov.cy/DrcorPublic/SearchForm.aspx"

# Step 1: Execute the search
response = requests.post(search_url, data=search_params)

# Step 2: Check if the request was successful
if response.status_code == 200:
    print("Search executed successfully.")
    # Save the updated HTML content of the results page
    with open('search_results.html', 'w', encoding='utf-8') as results_file:
        results_file.write(response.text)
    print("Search results saved to 'search_results.html'.")
else:
    print(f"Failed to execute search. Status code: {response.status_code}")