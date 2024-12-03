# filename: search_bank_of_cyprus.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Step 1: Set up the Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Step 2: Open the provided URL
url = "https://efiling.drcor.mcit.gov.cy/DrcorPublic/SearchForm.aspx?sc=0&cultureInfo=en-AU"
driver.get(url)

# Step 3: Locate the input text field and enter the search term
search_input = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucSearch_txtName")
search_input.send_keys("BANK OF CYPRUS PUBLIC COMPANY LIMITED")

# Step 4: Print all clickable elements to identify the search button
clickable_elements = driver.find_elements(By.XPATH, "//*[@onclick] | //a | //button | //input[@type='button'] | //input[@type='submit']")
for element in clickable_elements:
    print(f"Tag: {element.tag_name}, Type: {element.get_attribute('type')}, Value: {element.get_attribute('value')}, Text: {element.text}, ID: {element.get_attribute('id')}, Name: {element.get_attribute('name')}, OnClick: {element.get_attribute('onclick')}")

# Note: Based on the printed output, you need to identify the correct element for the search functionality.
# Once identified, you can modify the script to click the correct element and proceed with the search process.

# Close the WebDriver
driver.quit()