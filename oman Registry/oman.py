import json
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

# Create directory for output files
output_dir = 'Housing_bank_details'
os.makedirs(output_dir, exist_ok=True)

# Initialize the Selenium web driver
driver = webdriver.Chrome()  # Ensure you have the correct driver installed
driver.get("https://www.business.gov.om/portal/searchEstablishments")

# Language selection
language_selector = "#header > div > div > div.submenu-line.pull-right > div > a"
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, language_selector))).click()

# Perform search
search_input = driver.find_element(By.ID, "search_company_name")
search_input.send_keys("بنك الاسكان العماني")

# Handle Captcha
time.sleep(10)  # Wait for human interaction

# Submit Search
search_button = driver.find_element(By.CSS_SELECTOR, "#searchCompanyForm > div > div.row > div:nth-child(5) > button")
search_button.click()

# Wait for result to load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div/div/div/table")))

# Navigate to Results
results_table = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div/div/table")
rows = results_table.find_elements(By.TAG_NAME, "tr")

# Check for exact match
exact_match_found = False
for row in rows:
    if "بنك الاسكان العماني" in row.text:
        view_button = row.find_element(By.LINK_TEXT, "View")
        view_button.click()
        exact_match_found = True
        break

# Pagination handling if no exact match found
if not exact_match_found:
    while True:
        pagination = driver.find_elements(By.XPATH, "/html/body/div[2]/div[2]/div/div/div/ul")
        if pagination:
            next_page = pagination[0].find_element(By.LINK_TEXT, "Next")
            if next_page.get_attribute("href") != "#":
                next_page.click()
                time.sleep(2)  # Wait for the page to load
                rows = driver.find_elements(By.XPATH, "/html/body/div[2]/div[2]/div/div/div/table/tr")
                for row in rows:
                    if "بنك الاسكان العماني" in row.text:
                        view_button = row.find_element(By.LINK_TEXT, "View")
                        view_button.click()
                        exact_match_found = True
                        break
            else:
                break
        else:
            break

# Scrape Details from Tabs
data = {
    "Commercial Name": [],
    "Legal Type": [],
    "Registry Information": [],
    "Address": [],
    "Contact Information": [],
    "Capital": [],
    "Fiscal Information": [],
    "Business Activities": [],
    "Investors": [],
    "Authorized Signatories": [],
    "Auditor": [],
    "Licenses": []
}

# Function to scrape tab data
def scrape_tab(tab_xpath, data_selector, data_key):
    try:
        tab = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, tab_xpath)))
        if "collapsed" in tab.get_attribute("class"):
            tab.click()
        data_element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, data_selector)))
        data[data_key].append(data_element.text)
    except Exception as e:
        print(f"Error scraping {data_key}: {e}")
        # Print the current page source for debugging
        try:
            print(driver.page_source.encode('utf-8').decode('utf-8'))  # Encode to avoid Unicode errors
        except Exception as inner_e:
            print(f"Failed to print page source: {inner_e}")

# Scrape each tab
scrape_tab("/html/body/div[2]/div[2]/div[2]/div[2]/div[1]/h2/a", "#commercialNameSection > div > div", "Commercial Name")
scrape_tab("/html/body/div[2]/div[2]/div[2]/div[3]/div[1]/h2/a", "#legalTypeSection > div > div", "Legal Type")
scrape_tab("/html/body/div[2]/div[2]/div[2]/div[4]/div[1]/h2/a", "#registryInformationSection > div > div", "Registry Information")
scrape_tab("/html/body/div[2]/div[2]/div[2]/div[5]/div[1]/h2/a", "#companyAddressSection > div > div", "Address")
scrape_tab("/html/body/div[2]/div[2]/div[2]/div[6]/div[1]/h2/a", "#contactInformationSection > div > div > div:nth-child(1)", "Contact Information")
scrape_tab("/html/body/div[2]/div[2]/div[2]/div[7]/div[1]/h2/a", "#capitalSection > div > div", "Capital")
scrape_tab("/html/body/div[2]/div[2]/div[2]/div[8]/div[1]/h2/a", "#fiscalInformationSection > div > div", "Fiscal Information")
scrape_tab("/html/body/div[2]/div[2]/div[2]/div[9]/div[1]/h2/a", "#declaredActivitiesSection > div > div", "Business Activities")

# Check for Investors tab
try:
    investors_tab_xpath = "/html/body/div[2]/div[2]/div[2]/div[10]/div[1]/h2/a"
    investors_data_selector = "#investorsSection > div > div"
    scrape_tab(investors_tab_xpath, investors_data_selector, "Investors")
except Exception as e:
    print("Investors tab not found or could not be scraped.")
    print(driver.page_source.encode('utf-8').decode('utf-8'))  # Print the page source for debugging

# Check for Authorized Signatories tab
try:
    signatories_tab_xpath = "/html/body/div[2]/div[2]/div[2]/div[11]/div[1]/h2/a"
    signatories_data_selector = "#signatoriesSection > div > div"
    scrape_tab(signatories_tab_xpath, signatories_data_selector, "Authorized Signatories")
except Exception as e:
    print("Authorized Signatories tab not found or could not be scraped.")
    print(driver.page_source.encode('utf-8').decode('utf-8'))  # Print the page source for debugging

# Check for Auditor tab
try:
    auditor_tab_xpath = "/html/body/div[2]/div[2]/div[2]/div[12]/div[1]/h2/a"
    auditor_data_selector = "#auditorsSection > div > div"
    scrape_tab(auditor_tab_xpath, auditor_data_selector, "Auditor")
except Exception as e:
    print("Auditor tab not found or could not be scraped.")
    print(driver.page_source.encode('utf-8').decode('utf-8'))  # Print the page source for debugging

# Check for Licenses tab
try:
    licenses_tab_xpath = "/html/body/div[2]/div[2]/div[2]/div[13]/div[1]/h2/a"
    licenses_data_selector = "#licenseSection > div > table"
    scrape_tab(licenses_tab_xpath, licenses_data_selector, "Licenses")
except Exception as e:
    print("Licenses tab not found or could not be scraped.")
    print(driver.page_source.encode('utf-8').decode('utf-8'))  # Print the page source for debugging

# Save data to JSON file
with open(os.path.join(output_dir, 'output.json'), 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

# Clean Up
driver.quit()