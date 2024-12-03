# filename: scrape_bank_of_cyprus_selenium.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up the Selenium WebDriver (make sure you have the appropriate WebDriver installed, e.g., chromedriver)
driver = webdriver.Chrome()

# Open the website
driver.get("https://efiling.drcor.mcit.gov.cy/DrcorPublic/SearchForm.aspx?sc=0&cultureInfo=en-AU")

# Wait for the search input field to be present
search_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "ctl00_MainContent_txtName"))
)

# Enter the company name
search_input.send_keys("BANK OF CYPRUS PUBLIC COMPANY LIMITED")

# Wait for the search button to be present and click it
search_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "ctl00_MainContent_btnSearch"))
)
search_button.click()

# Wait for the search results to load
time.sleep(5)

# Find the search results table
results_table = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "ctl00_MainContent_gvResults"))
)

# Extract the details of the company
company_details = ""
rows = results_table.find_elements(By.TAG_NAME, "tr")
for row in rows[1:]:  # Skip the header row
    columns = row.find_elements(By.TAG_NAME, "td")
    if columns[0].text.strip() == "BANK OF CYPRUS PUBLIC COMPANY LIMITED":
        company_details = "\n".join([col.text.strip() for col in columns])
        break

# Save the details to a text file
with open('bank_of_cyprus_details.txt', 'w') as file:
    file.write(company_details)

print("Details of BANK OF CYPRUS PUBLIC COMPANY LIMITED have been saved to 'bank_of_cyprus_details.txt'.")

# Close the browser
driver.quit()