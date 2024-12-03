# filename: simulate_search_without_driver.py
import requests
from bs4 import BeautifulSoup

# URL for the search action
url = "https://efiling.drcor.mcit.gov.cy/DrcorPublic/SearchForm.aspx?sc=0&cultureInfo=en-AU"

# Prepare the data for the POST request
data = {
    "__VIEWSTATE": "",  # You may need to fetch this value from the initial page
    "__VIEWSTATEGENERATOR": "",  # Fetch this value as well
    "__PREVIOUSPAGE": "",  # Fetch this value as well
    "__EVENTVALIDATION": "",  # Fetch this value as well
    "ctl00$cphMyMasterCentral$ucSearch$txtName": "BANK OF CYPRUS PUBLIC COMPANY LIMITED",
    "ctl00$cphMyMasterCentral$ucSearch$txtNumber": "",  # Leave empty if not searching by number
    "ctl00$cphMyMasterCentral$ucSearch$optStartMatch": "on",  # If applicable
    "ctl00$cphMyMasterCentral$ucSearch$optEndMatch": "on",  # If applicable
    "ctl00$cphMyMasterCentral$ucSearch$optSoundLike": "on",  # If applicable
    "ctl00$cphMyMasterCentral$ucSearch$lbtnSearch": "Go"  # The button that triggers the search
}

# Fetch the initial page to get the necessary hidden fields
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Extract the necessary hidden fields
data["__VIEWSTATE"] = soup.find(id="__VIEWSTATE")["value"]
data["__VIEWSTATEGENERATOR"] = soup.find(id="__VIEWSTATEGENERATOR")["value"]
data["__PREVIOUSPAGE"] = soup.find(id="__PREVIOUSPAGE")["value"]
data["__EVENTVALIDATION"] = soup.find(id="__EVENTVALIDATION")["value"]

# Send the POST request with the search data
search_response = requests.post(url, data=data)

# Check if the search was successful
if search_response.status_code == 200:
    # Save the updated HTML for further analysis
    with open("search_results.html", "w", encoding='utf-8') as file:
        file.write(search_response.text)
    print("Search completed and results saved to search_results.html.")
else:
    print("Failed to perform the search. Status code:", search_response.status_code)