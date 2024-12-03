# filename: perform_search.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Set up the WebDriver (make sure to specify the correct path to your WebDriver)
service = Service('C:/WebDriver/chromedriver.exe')  # Update this path to your actual ChromeDriver
driver = webdriver.Chrome(service=service)

# Navigate to the search page
driver.get("https://efiling.drcor.mcit.gov.cy/DrcorPublic/SearchForm.aspx?sc=0&cultureInfo=en-AU")

# Wait for the page to load
time.sleep(2)

# Input the search query
name_input = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucSearch_txtName")
number_input = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucSearch_txtNumber")

# Fill in the search fields
name_input.send_keys("BLACK JACK SPORTS BETTING")
number_input.send_keys("")  # Assuming we are not searching by number

# Trigger the search
search_button = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucSearch_lbtnSearch")
search_button.click()

# Wait for the results to load
time.sleep(5)

# Optionally, you can fetch the updated HTML after the search
updated_html = driver.page_source

# Save the updated HTML for further analysis
with open("updated_search_results.html", "w", encoding="utf-8") as file:
    file.write(updated_html)

# Close the browser
driver.quit()

print("Search executed and results saved.")