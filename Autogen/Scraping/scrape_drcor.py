# filename: scrape_drcor.py

import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Set up the Selenium WebDriver
driver = webdriver.Chrome()  # You can use any other driver like Firefox, Edge etc.
driver.get("https://efiling.drcor.mcit.gov.cy/DrcorPublic/?cultureInfo=en-AU")

# Wait for the search input to be present
wait = WebDriverWait(driver, 10)
search_input = wait.until(EC.presence_of_element_located((By.ID, "ctl00_ctl00_PlaceHolderMain_PlaceHolderMain_SearchControl1_txtName")))

# Enter the search criteria
search_input.send_keys("jack")
search_input.send_keys(Keys.RETURN)

# Wait for the results to load and display the links
results = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".gridViewRow a")))

# Click on the first result link
first_result_link = results[0]
first_result_link.click()

# Wait for the details page to load
details_page = wait.until(EC.presence_of_element_located((By.ID, "ctl00_ctl00_PlaceHolderMain_PlaceHolderMain_EntityDetails1_lblName")))

# Parse the details page with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Extract the required details
name = soup.find(id="ctl00_ctl00_PlaceHolderMain_PlaceHolderMain_EntityDetails1_lblName").text.strip()
reg_number = soup.find(id="ctl00_ctl00_PlaceHolderMain_PlaceHolderMain_EntityDetails1_lblRegNumber").text.strip()
entity_type = soup.find(id="ctl00_ctl00_PlaceHolderMain_PlaceHolderMain_EntityDetails1_lblEntityType").text.strip()
name_status = soup.find(id="ctl00_ctl00_PlaceHolderMain_PlaceHolderMain_EntityDetails1_lblNameStatus").text.strip()
org_status = soup.find(id="ctl00_ctl00_PlaceHolderMain_PlaceHolderMain_EntityDetails1_lblOrgStatus").text.strip()

# Close the WebDriver
driver.quit()

# Create a dictionary with the extracted data
data = {
    "Name": name,
    "Reg. Number": reg_number,
    "Type": entity_type,
    "Name Status": name_status,
    "Organisation Status": org_status
}

# Convert the dictionary to JSON format
json_data = json.dumps(data, indent=4)
print(json_data)