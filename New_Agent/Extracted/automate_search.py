# filename: automate_search.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# Set up the Selenium WebDriver (make sure to specify the correct path to your WebDriver)
service = Service('C:\\WebDrivers\\chromedriver.exe')  # Update this path to your ChromeDriver
driver = webdriver.Chrome(service=service)

# Open the search page
driver.get("https://efiling.drcor.mcit.gov.cy/DrcorPublic/SearchForm.aspx?sc=0&cultureInfo=en-AU")

# Wait for the page to load
time.sleep(2)

# Fill in the search fields
name_input = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucSearch_txtName")
number_input = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucSearch_txtNumber")

# Enter the search query
name_input.send_keys("BLACK JACK SPORTS BETTING")
# If you want to search by number, you can uncomment the next line and provide a value
# number_input.send_keys("Your ID or Number Here")

# Click the search button
search_button = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucSearch_lbtnSearch")
search_button.click()

# Wait for results to load
time.sleep(5)

# Optionally, you can fetch the updated HTML after the search
updated_html = driver.page_source
with open("search_results.html", "w", encoding='utf-8') as file:
    file.write(updated_html)

print("Search executed and results saved to 'search_results.html'.")

# Close the browser
driver.quit()