# filename: web_scraping.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import json
import time

# Initialize the webdriver
driver = webdriver.Chrome()

# Open the URL
url = "{url}"
driver.get(url)

# Wait for the language selection and choose "English"
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'English')]"))).click()

# Navigate to the search tab
search_tab = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Search')]")))
search_tab.click()

# Select "with all these words" in the search criteria
search_criteria = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//select[@name='searchCriteria']")))
search_criteria.click()
search_criteria.send_keys("with all these words")
search_criteria.send_keys(Keys.RETURN)

# Enter "cedar rose" in the Name field
name_field = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='name']")))
name_field.send_keys("cedar rose")

# Click the "Go" button
go_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Go']")))
go_button.click()

# Wait for the table to load and extract the data
table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//table[@id='results']")))
rows = table.find_elements(By.TAG_NAME, "tr")

# Extract the data from the table
data = []
for row in rows[1:]:  # Skip the header row
    cols = row.find_elements(By.TAG_NAME, "td")
    entry = {
        "Name": cols[0].text,
        "Reg. Number": cols[1].text,
        "Type": cols[2].text,
        "Name Status": cols[3].text,
        "Organisation Status": cols[4].text
    }
    data.append(entry)

# Close the driver
driver.quit()

# Print the data in JSON format
print(json.dumps(data, indent=4))