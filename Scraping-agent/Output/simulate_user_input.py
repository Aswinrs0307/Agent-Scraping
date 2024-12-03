# filename: simulate_user_input.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Set up the WebDriver (make sure to specify the correct path to your WebDriver)
service = Service('C:/path/to/chromedriver.exe')  # Update this path
driver = webdriver.Chrome(service=service)

# Open the target URL
driver.get("https://efiling.drcor.mcit.gov.cy/DrcorPublic/SearchForm.aspx?sc=0&cultureInfo=en-AU")

# Wait for the page to load
time.sleep(2)

# Locate the input fields
name_input = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucSearch_txtName")
number_input = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucSearch_txtNumber")

# Simulate user input
name_input.send_keys("BANK OF CYPRUS PUBLIC COMPANY LIMITED")
# If you have a number to search, you can uncomment the next line and provide the number
# number_input.send_keys("Your ID Here")

# Locate and click the search trigger
search_trigger = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucSearch_lbtnSearch")
search_trigger.click()

# Wait for the results to load
time.sleep(5)

# Optionally, you can fetch the updated HTML after the search
updated_html = driver.page_source

# Save the updated HTML for further analysis
with open("search_results.html", "w", encoding='utf-8') as file:
    file.write(updated_html)

# Close the WebDriver
driver.quit()

print("Search completed and results saved to search_results.html.")