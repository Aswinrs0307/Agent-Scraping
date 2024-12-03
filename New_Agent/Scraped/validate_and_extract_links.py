# filename: validate_and_extract_links.py
import requests

# List of result links extracted from the previous step
result_links = [
    {'href': 'https://eforms.eservices.cyprus.gov.cy/MCIT/RCOR/OrganisationFileSearch', 'text': 'Study File'},
    {'href': 'OrganizationNameExamination.aspx', 'text': 'Results of Name Examination'},
    # Add more relevant links as needed
]

# Validate and extract links
valid_links = []
for link in result_links:
    href = link['href']
    if href.startswith('http') or href.startswith('https'):
        # Check if the link is valid
        try:
            response = requests.head(href, allow_redirects=True)
            if response.status_code == 200:
                valid_links.append(link)
        except requests.RequestException as e:
            print(f"Error validating link {href}: {e}")
    else:
        # Handle relative links
        print(f"Relative link found: {href}")

# Print valid links
print("Valid Links:")
for valid_link in valid_links:
    print(valid_link)