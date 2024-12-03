# filename: navigate_grid_content.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
name_input.send_keys("BLACK JACK SPORTS BETTING")

# Click the search button
search_button = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucSearch_lbtnSearch")
search_button.click()

# Wait for results to load
time.sleep(5)

# Write the page source to a file for inspection
with open("page_source.html", "w", encoding='utf-8') as file:
    file.write(driver.page_source)

print("Page source saved to 'page_source.html' for inspection.")

# Wait for the "Select" link to be clickable
try:
    select_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '__doPostBack') and contains(text(), 'Select')]"))
    )

    # Scroll into view and click the "Select" link
    driver.execute_script("arguments[0].scrollIntoView();", select_link)
    select_link.click()

    # Wait for the new page to load
    time.sleep(5)

    # Optionally, you can fetch the updated HTML after the navigation
    updated_html = driver.page_source
    with open("navigated_results.html", "w", encoding='utf-8') as file:
        file.write(updated_html)

    print("Navigated through the link and results saved to 'navigated_results.html'.")

except Exception as e:
    print(f"An error occurred: {e}")

# Close the browser
driver.quit()