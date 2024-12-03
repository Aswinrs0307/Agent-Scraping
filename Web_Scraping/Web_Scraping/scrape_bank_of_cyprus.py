# filename: scrape_bank_of_cyprus.py

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Step 1: Scrape the HTML content of the provided URL
url = "https://efiling.drcor.mcit.gov.cy/DrcorPublic/SearchForm.aspx?sc=0&cultureInfo=en-AU"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Step 2: Extract the IDs, names, and class names of the text fields for searching input
text_fields = soup.find_all('input', {'type': 'text'})
for field in text_fields:
    print(f"ID: {field.get('id')}, Name: {field.get('name')}, Class: {field.get('class')}")

# Step 3: Identify and click the search button using Selenium
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(url)

# Wait for the page to load completely
wait = WebDriverWait(driver, 10)

# Initialize search_input as None
search_input = None

# Check if the element is inside an iframe
iframes = driver.find_elements(By.TAG_NAME, 'iframe')
for iframe in iframes:
    driver.switch_to.frame(iframe)
    try:
        search_input = wait.until(EC.presence_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_txtName')))
        break
    except:
        driver.switch_to.default_content()

# If search_input is still None, try to find it in the main content
if search_input is None:
    try:
        search_input = wait.until(EC.presence_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_txtName')))
    except:
        print("Search input field not found.")
        driver.quit()
        exit(1)

# Find the search input field and enter the search term
search_input.send_keys("BANK OF CYPRUS PUBLIC COMPANY LIMITED")

# Find the search button and click it
search_button = wait.until(EC.element_to_be_clickable((By.ID, 'ctl00_ContentPlaceHolder1_btnSearch')))
search_button.click()

# Wait for the search results to load
time.sleep(5)

# Step 4: Scrape the search results page
search_results_page = driver.page_source
soup_results = BeautifulSoup(search_results_page, 'html.parser')

# Step 5: Extract and open the link related to "BANK OF CYPRUS PUBLIC COMPANY LIMITED"
link = soup_results.find('a', text="BANK OF CYPRUS PUBLIC COMPANY LIMITED")
if link:
    company_url = "https://efiling.drcor.mcit.gov.cy/DrcorPublic/" + link['href']
    driver.get(company_url)

    # Wait for the company details page to load
    time.sleep(5)

    # Step 6: Scrape the details from the final page
    company_page = driver.page_source
    soup_company = BeautifulSoup(company_page, 'html.parser')

    # Extract the details of BANK OF CYPRUS PUBLIC COMPANY LIMITED
    details = soup_company.find('div', {'id': 'ctl00_ContentPlaceHolder1_divCompanyDetails'})
    if details:
        print("Details of BANK OF CYPRUS PUBLIC COMPANY LIMITED:")
        print(details.get_text(strip=True))
    else:
        print("Details not found.")
else:
    print("Company link not found.")

# Close the browser
driver.quit()