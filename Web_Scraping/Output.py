# filename: scrape_bank_of_cyprus.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Step 1: Set up the Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://efiling.drcor.mcit.gov.cy/DrcorPublic/SearchForm.aspx?sc=0&cultureInfo=en-AU")

# Step 2: Find the text input field and enter the name
search_input = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucSearch_txtName")
search_input.send_keys("BANK OF CYPRUS PUBLIC COMPANY LIMITED")

# Step 3: Submit the form (assuming Enter key works to submit)
search_input.send_keys(Keys.RETURN)

# Wait for the search results to load
time.sleep(15)  # Increase wait time to ensure results are loaded

# Step 4: Scrape the search results page
html_content = driver.page_source
soup = BeautifulSoup(html_content, 'html.parser')

# Find links related to "BANK OF CYPRUS PUBLIC COMPANY LIMITED"
results = soup.find_all('a', string="BANK OF CYPRUS PUBLIC COMPANY LIMITED")

if results:
    # Open the first result link
    result_link = results[0].get('href')
    driver.get(result_link)

    # Wait for the details page to load
    time.sleep(15)  # Increase wait time to ensure details page is loaded

    # Scrape the details page
    details_html_content = driver.page_source
    details_soup = BeautifulSoup(details_html_content, 'html.parser')

    # Extract details (assuming details are in a specific div or table)
    details_div = details_soup.find('div', {'id': 'details'})
    if details_div:
        details_text = details_div.get_text(separator='\n')
        print("Details of BANK OF CYPRUS PUBLIC COMPANY LIMITED:")
        print(details_text)
    else:
        print("Details not found.")
else:
    print("No results found for BANK OF CYPRUS PUBLIC COMPANY LIMITED.")

# Close the browser
driver.quit()