# filename: scrape_bank_of_cyprus.py
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def log(message):
    print(f"[LOG] {message}")

try:
    # Step 1: Scrape the HTML content of the provided URL
    url = "https://efiling.drcor.mcit.gov.cy/DrcorPublic/SearchForm.aspx?sc=0&cultureInfo=en-AU"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    log("HTML content scraped successfully.")

    # Step 2: Extract the IDs, names, and class names of the text fields for searching input
    input_fields = soup.find_all('input', {'type': 'text'})
    for field in input_fields:
        log(f"ID: {field.get('id')}, Name: {field.get('name')}, Class: {field.get('class')}")

    # Step 3: Identify and click the search button using Selenium
    driver = webdriver.Chrome()  # Ensure you have the ChromeDriver installed and in your PATH
    driver.get(url)
    log("Web page loaded successfully.")

    # Wait for the iframe to be present and switch to it if necessary
    try:
        iframe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
        driver.switch_to.frame(iframe)
        log("Switched to iframe.")
    except:
        log("No iframe found, continuing without switching.")

    # Find the search input field and enter the company name
    try:
        search_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_txtName')))
        search_input.send_keys("BANK OF CYPRUS PUBLIC COMPANY LIMITED")
        log("Search input field located and company name entered.")
    except Exception as e:
        log(f"Error locating search input field: {e}")
        driver.quit()
        exit(1)

    # Find the search button and click it
    try:
        search_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'ctl00_ContentPlaceHolder1_btnSearch')))
        search_button.click()
        log("Search button located and clicked.")
    except Exception as e:
        log(f"Error locating search button: {e}")
        driver.quit()
        exit(1)

    # Wait for the results page to load
    time.sleep(5)
    log("Results page loaded.")

    # Step 4: Scrape the search results page
    results_soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Step 5: Extract the link related to "BANK OF CYPRUS PUBLIC COMPANY LIMITED"
    company_link = None
    for link in results_soup.find_all('a', href=True):
        if "BANK OF CYPRUS PUBLIC COMPANY LIMITED" in link.text:
            company_link = link['href']
            break

    if company_link:
        log(f"Company link found: {company_link}")
        # Step 6: Scrape the details from the extracted link
        driver.get(company_link)
        time.sleep(5)
        company_soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Extract the details of the company
        company_details = company_soup.get_text()

        # Step 7: Output the details in text format
        print("Details of BANK OF CYPRUS PUBLIC COMPANY LIMITED:")
        print(company_details)
    else:
        log("Company link not found.")

    driver.quit()
except Exception as e:
    log(f"An error occurred: {e}")