# filename: simulate_search.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Initialize the WebDriver (make sure to have the appropriate driver installed)
driver = webdriver.Chrome()  # Adjust if using a different browser

try:
    # Step 4: Open the search page
    driver.get("https://efiling.drcor.mcit.gov.cy/DrcorPublic/SearchForm.aspx?sc=0&cultureInfo=en-AU")
    
    # Step 4.1: Enter the search term into the input field
    name_input = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucSearch_txtName")
    name_input.send_keys("BANK OF CYPRUS PUBLIC COMPANY LIMITED")
    
    # Step 4.2: Simulate clicking the search trigger
    search_button = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucSearch_lbtnSearch")
    search_button.click()
    
    # Wait for the results to load
    time.sleep(5)  # Adjust time as necessary for the page to load

    # Step 5: Fetch the updated HTML after the search
    updated_html = driver.page_source
    with open("search_results.html", "w", encoding="utf-8") as file:
        file.write(updated_html)
    print("Search results successfully written to search_results.html")

finally:
    driver.quit()