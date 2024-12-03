# filename: scrape_bank_of_cyprus.py

import requests
from bs4 import BeautifulSoup

# Step 1: Scrape the HTML content of the provided URL
url = "https://efiling.drcor.mcit.gov.cy/DrcorPublic/SearchForm.aspx?sc=0&cultureInfo=en-AU"
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    html_content = response.text
else:
    print("Failed to retrieve the webpage.")
    exit()

# Step 2: Parse the HTML to find all input fields (text fields) and extract their IDs, names, and class names
soup = BeautifulSoup(html_content, 'html.parser')
input_fields = soup.find_all('input', {'type': 'text'})

# Extract IDs, names, and class names
fields_info = []
for input_field in input_fields:
    field_id = input_field.get('id', 'N/A')
    field_name = input_field.get('name', 'N/A')
    field_class = input_field.get('class', 'N/A')
    fields_info.append({'id': field_id, 'name': field_name, 'class': field_class})

# Print the extracted information
print("Extracted input fields information:")
for field in fields_info:
    print(f"ID: {field['id']}, Name: {field['name']}, Class: {field['class']}")

# Extract hidden input fields required for form submission
hidden_inputs = soup.find_all('input', {'type': 'hidden'})
form_data = {hidden_input['name']: hidden_input['value'] for hidden_input in hidden_inputs}

# Add search-specific data
form_data['ctl00$cphMyMasterCentral$ucSearch$txtName'] = 'BANK OF CYPRUS PUBLIC COMPANY LIMITED'
form_data['ctl00$cphMyMasterCentral$ucSearch$btnSearch'] = 'Search'

# Step 3: Perform a search for "BANK OF CYPRUS PUBLIC COMPANY LIMITED"
search_url = "https://efiling.drcor.mcit.gov.cy/DrcorPublic/SearchForm.aspx"
search_response = requests.post(search_url, data=form_data)

# Check if the search request was successful
if search_response.status_code == 200:
    search_html_content = search_response.text
    # Write the search results HTML content to a file for debugging
    try:
        with open("search_results.html", "w", encoding="utf-8") as file:
            file.write(search_html_content)
        print("Search results HTML content written to search_results.html")
    except Exception as e:
        print(f"Failed to write HTML content to file: {e}")
        exit()
else:
    print("Failed to perform the search.")
    exit()

# Step 4: Parse the search results to find the link to the details page
search_soup = BeautifulSoup(search_html_content, 'html.parser')
details_link = search_soup.find('a', text='BANK OF CYPRUS PUBLIC COMPANY LIMITED')

if details_link:
    details_url = "https://efiling.drcor.mcit.gov.cy" + details_link['href']
    details_response = requests.get(details_url)

    # Check if the details request was successful
    if details_response.status_code == 200:
        details_html_content = details_response.text
    else:
        print("Failed to retrieve the details page.")
        exit()
else:
    print("Failed to find the details link.")
    exit()

# Step 5: Extract and retrieve the details of "BANK OF CYPRUS PUBLIC COMPANY LIMITED"
details_soup = BeautifulSoup(details_html_content, 'html.parser')
company_details = details_soup.find('div', {'id': 'ctl00_MainContent_divCompanyDetails'})

if company_details:
    company_info = company_details.get_text(separator='\n', strip=True)
else:
    company_info = "Failed to retrieve company details."

# Step 6: Output the details in a text format
print("Details of BANK OF CYPRUS PUBLIC COMPANY LIMITED:")
print(company_info)