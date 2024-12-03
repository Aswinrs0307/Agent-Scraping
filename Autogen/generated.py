from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Set up the Selenium WebDriver (make sure you have the appropriate driver installed, e.g., chromedriver)
driver = webdriver.Chrome()

try:
    # Step 1: Go to the URL
    driver.get("https://efiling.drcor.mcit.gov.cy/")

    # Step 2: Select Language as "English"
    english_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'English')]"))
    )
    english_button.click()

    # Step 3: Navigate to the search tab
    search_tab = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Search')]"))
    )
    search_tab.click()

    # Step 4: In Search Criteria choose "with all these words"
    search_criteria = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//select[@name='criteria']"))
    )
    search_criteria.send_keys("with all these words")

    # Step 5: In Name type "cedar rose"
    name_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@name='name']"))
    )
    name_input.send_keys("cedar rose")

    # Step 6: Click "Go" button
    go_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@value='Go']"))
    )
    go_button.click()

    # Step 7: Wait for the table to load and extract the data
    time.sleep(5)  # Adjust the sleep time if necessary
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find('table', {'class': 'results'})  # Adjust the class name if necessary

    # Step 8: Extract the data from the table
    data = []
    for row in table.find_all('tr')[1:]:  # Skip the header row
        cols = row.find_all('td')
        data.append({
            "Name": cols[0].text.strip(),
            "Reg. Number": cols[1].text.strip(),
            "Type": cols[2].text.strip(),
            "Name Status": cols[3].text.strip(),
            "Organisation Status": cols[4].text.strip()
        })

    # Print the extracted data
    for entry in data:
        print(entry)

finally:
    # Close the WebDriver
    driver.quit()