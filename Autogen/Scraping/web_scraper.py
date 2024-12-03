# filename: web_scraper.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import json
import time

# Initialize the WebDriver
driver = webdriver.Chrome()

try:
    # Step 1: Go to the URL
    url = "http://example.com"  # Replace with the actual URL
    driver.get(url)

    # Step 2: Select Language as "English"
    language_dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "language-dropdown-id"))  # Replace with the actual ID
    )
    language_dropdown.click()
    english_option = driver.find_element(By.XPATH, "//option[text()='English']")
    english_option.click()

    # Step 3: Navigate to the search tab
    search_tab = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "search-tab-id"))  # Replace with the actual ID
    )
    search_tab.click()

    # Step 4: Choose "with all these words" in Search Criteria
    search_criteria = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "search-criteria-id"))  # Replace with the actual ID
    )
    search_criteria.click()
    all_words_option = driver.find_element(By.XPATH, "//option[text()='with all these words']")
    all_words_option.click()

    # Step 5: Type "cedar rose" in Name
    name_input = driver.find_element(By.ID, "name-input-id")  # Replace with the actual ID
    name_input.send_keys("cedar rose")

    # Step 6: Click "Go" button
    go_button = driver.find_element(By.ID, "go-button-id")  # Replace with the actual ID
    go_button.click()

    # Wait for the table to load
    time.sleep(5)

    # Step 7: Extract data from the table
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find('table', {'id': 'results-table-id'})  # Replace with the actual ID
    rows = table.find_all('tr')

    data = []
    for row in rows[1:]:  # Skip the header row
        cols = row.find_all('td')
        data.append({
            "Name": cols[0].text.strip(),
            "Reg. Number": cols[1].text.strip(),
            "Type": cols[2].text.strip(),
            "Name Status": cols[3].text.strip(),
            "Organisation Status": cols[4].text.strip()
        })

    # Step 8: Output the data in JSON format
    print(json.dumps(data, indent=4))

finally:
    driver.quit()