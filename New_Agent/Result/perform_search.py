# filename: perform_search.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Set up the Selenium WebDriver (make sure to have the appropriate driver installed)
driver = webdriver.Chrome()  # or webdriver.Firefox(), etc.

try:
    # Open the search form page
    driver.get("https://efiling.drcor.mcit.gov.cy/DrcorPublic/SearchForm.aspx?sc=0&cultureInfo=en-AU")

    # Wait for the page to load
    time.sleep(2)

    # Locate the input fields
    name_input = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucSearch_txtName")
    number_input = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucSearch_txtNumber")

    # Clear the input fields
    name_input.clear()
    number_input.clear()

    # Enter the search query
    name_input.send_keys("BLACK JACK SPORTS BETTING")

    # Locate and click the search button
    search_button = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucSearch_lbtnSearch")
    search_button.click()

    # Wait for the results to load
    time.sleep(5)

    # Fetch the updated HTML content after the search
    updated_html = driver.page_source

    # Save the updated HTML to a file
    with open("search_results.html", "w", encoding="utf-8") as file:
        file.write(updated_html)

    print("Search performed and results saved to search_results.html")

finally:
    # Close the browser
    driver.quit()