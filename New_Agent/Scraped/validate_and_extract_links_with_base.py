# filename: validate_and_extract_links_with_base.py
import requests
from urllib.parse import urljoin

# Base URL of the website
base_url = "https://efiling.drcor.mcit.gov.cy/"

# List of result links extracted from the previous step
result_links = [
    {'href': 'https://eforms.eservices.cyprus.gov.cy/MCIT/RCOR/OrganisationFileSearch', 'text': 'Study File'},
    {'href': 'OrganizationNameExamination.aspx', 'text': 'Results of Name Examination'},
]

# Validate and extract links
valid_links = []
for link in result_links:
    href = link['href']
    # Construct full URL for relative links
    full_url = urljoin(base_url, href)
    
    # Check if the link is valid
    try:
        response = requests.head(full_url, allow_redirects=True)
        if response.status_code == 200:
            valid_links.append({'href': full_url, 'text': link['text']})
    except requests.RequestException as e:
        print(f"Error validating link {full_url}: {e}")

# Print valid links
print("Valid Links:")
for valid_link in valid_links:
    print(valid_link)