# filename: navigate_and_extract.py
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

# Wait for the "Select" link to be clickable
select_link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '__doPostBack') and contains(text(), 'Select')]"))
)

# Scroll into view and click the "Select" link
driver.execute_script("arguments[0].scrollIntoView();", select_link)
select_link.click()

# Wait for the new page to load
time.sleep(5)

# Extract relevant information from the new page
# Adjust the selectors based on the actual content of the new page
# For example, if you want to extract text from specific elements:
details = driver.find_elements(By.XPATH, "//div[@class='details']")  # Adjust this XPath as needed

# Prepare to save the extracted information
extracted_info = []
for detail in details:
    extracted_info.append(detail.text)

# Save the extracted information to a text file
with open("extracted_details.txt", "w", encoding='utf-8') as file:
    for info in extracted_info:
        file.write(info + "\n")

print("Extracted details saved to 'extracted_details.txt'.")

# Close the browser
driver.quit()