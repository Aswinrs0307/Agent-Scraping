# filename: automate_search.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Set up the Selenium WebDriver (make sure to have the appropriate driver installed)
driver = webdriver.Chrome()  # You can use Firefox() or any other browser driver

# Open the target URL
driver.get("https://efiling.drcor.mcit.gov.cy/DrcorPublic/SearchForm.aspx?sc=0&cultureInfo=en-AU")

# Wait for the page to load
time.sleep(3)

# Input the search query into the name field
name_field = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucSearch_txtName")
name_field.send_keys("BLACK JACK SPORTS BETTING")

# If there's a number field, you can fill it as well (leave it empty if not needed)
number_field = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucSearch_txtNumber")
number_field.send_keys("")  # Leave empty for this example

# Click the search button
search_button = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucSearch_lbtnSearch")
search_button.click()

# Wait for the results to load
time.sleep(5)

# Optionally, you can fetch the updated HTML after the search
updated_html = driver.page_source

# Save the updated HTML for further analysis
with open("search_results.html", "w", encoding="utf-8") as file:
    file.write(updated_html)

print("Search executed and results saved.")

# Close the browser
driver.quit()