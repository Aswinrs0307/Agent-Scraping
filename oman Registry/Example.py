import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

url="https://www.business.gov.om/portal/searchEstablishments"
name="بنك الاسكان العماني"
# Create the output directory if it doesn't exist
output_dir = 'Housing_bank'
os.makedirs(output_dir, exist_ok=True)

# Initialize the Selenium web driver
driver = webdriver.Chrome()  # Ensure you have the correct driver installed
driver.get(url)

# Language selection
language_selector = driver.find_element(By.CSS_SELECTOR, "#header > div > div > div.submenu-line.pull-right > div > a")
language_selector.click()
time.sleep(2)  # Wait for the language to change

# Perform search
search_input = driver.find_element(By.ID, "search_company_name")
search_input.send_keys(name)

# Handle Captcha
print("Please complete the CAPTCHA within 10 seconds...")
time.sleep(10)

# Submit Search
search_button = driver.find_element(By.CSS_SELECTOR, "#searchCompanyForm > div > div.row > div:nth-child(5) > button")
search_button.click()

# Wait for result to load
try:
    # Wait for the results table to be visible
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//table")))
    print("Results table is visible.")
except Exception as e:
    print("Error: Results table not found. Check if the search was successful.")
    driver.quit()
    raise e

# Navigate to Results
results_table = driver.find_element(By.XPATH, "//table")
rows = results_table.find_elements(By.TAG_NAME, "tr")

# Check for exact match
exact_match_found = False
for row in rows:
    if name in row.text:
        view_button = row.find_element(By.TAG_NAME, "a")
        view_button.click()
        exact_match_found = True
        break

# If no exact match, handle pagination
if not exact_match_found:
    while True:
        # Check for matches in the current page
        for row in rows:
            if name in row.text:
                view_button = row.find_element(By.TAG_NAME, "a")
                view_button.click()
                exact_match_found = True
                break
        if exact_match_found:
            break

        # Check for pagination
        try:
            next_page = driver.find_element(By.XPATH, "//a[contains(text(), 'Next')]")
            if next_page.get_attribute("href") != "#":
                next_page.click()
                WebDriverWait(driver, 10).until(EC.staleness_of(rows[0]))  # Wait for the new page to load
                rows = driver.find_elements(By.TAG_NAME, "tr")  # Refresh rows
            else:
                break
        except Exception as e:
            print("No more pages or error:", e)
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
def scrape_tab(tab_xpath, details_selectors):
    try:
        tab = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, tab_xpath)))
        if "collapsed" in tab.get_attribute("class"):
            tab.click()  # Expand the tab
        time.sleep(1)  # Wait for the content to load
        details = {}
        for key, selector in details_selectors.items():
            details[key] = driver.find_element(By.CSS_SELECTOR, selector).text
        return details
    except Exception as e:
        print(f"Error scraping tab {tab_xpath}: {e}")
        return {}
# Function to scrape Licenses table data
def scrape_licenses():
    try:
        # Wait for the Licenses tab to be clickable and expand it if collapsed
        licenses_tab = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/div[2]/div[12]/div[1]/h2/a"))
        )
        if "collapsed" in licenses_tab.get_attribute("class"):
            licenses_tab.click()  # Expand the Licenses tab
            
        # Wait for the table to be visible
        table_body = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "#licenseSection > div > table > tbody"))
        )
        
        # Extract table headers
        headers = driver.find_elements(By.CSS_SELECTOR, "#licenseSection > div > table > thead th")
        header_names = [header.text for header in headers]
        
        # Extract table rows
        rows = table_body.find_elements(By.TAG_NAME, "tr")
        table_data = []
        
        for row in rows:
            columns = row.find_elements(By.TAG_NAME, "td")
            row_data = {}
            
            # Extract data for each row, assuming columns correspond to the header fields
            if len(columns) == len(header_names):
                for i, header in enumerate(header_names):
                    row_data[header] = columns[i].text
                table_data.append(row_data)
        
        return table_data
    except Exception as e:
        print(f"Error scraping Licenses table: {e}")
        return []

# Function to scrape Business Activities
def scrape_business_activities():
    try:
        # Click on the Business Activities tab
        business_activities_tab = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/div[2]/div[9]/div[1]/h2/a")))
        if "collapsed" in business_activities_tab.get_attribute("class"):
            business_activities_tab.click()  # Expand the tab
        time.sleep(1)  # Wait for the content to load

        # Extract the business activities table
        activities_table = driver.find_element(By.CSS_SELECTOR, "#declaredActivitiesSection > div > div > table")
        table_header = activities_table.find_element(By.TAG_NAME, "thead")
        headers = [th.text for th in table_header.find_elements(By.TAG_NAME, "th")]

        table_body = activities_table.find_element(By.TAG_NAME, "tbody")
        rows = table_body.find_elements(By.TAG_NAME, "tr")

        business_activities_data = []
        for row in rows:
            activity = {}
            cells = row.find_elements(By.TAG_NAME, "td")

            for i, cell in enumerate(cells):
                if i < len(headers):  # Only map if there's a corresponding header
                    activity[headers[i]] = cell.text

            business_activities_data.append(activity)

        return business_activities_data
    except Exception as e:
        print(f"Error scraping Business Activities: {e}")
        return []

# Function to scrape Investors
def scrape_investors():
    try:
        # Click on the Investors tab
        investors_tab = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/div[2]/div[10]/div[1]/h2/a")))
        if "collapsed" in investors_tab.get_attribute("class"):
            investors_tab.click()  # Expand the tab
        time.sleep(1)  # Wait for the content to load

        # Extract the investors table
        investors_table = driver.find_element(By.CSS_SELECTOR, "#investorsSection > div > div > table")
        table_header = investors_table.find_element(By.TAG_NAME, "thead")
        headers = [th.text for th in table_header.find_elements(By.TAG_NAME, "th")]

        table_body = investors_table.find_element(By.TAG_NAME, "tbody")
        rows = table_body.find_elements(By.TAG_NAME, "tr")

        investors_data = []
        for row in rows:
            investor = {}
            cells = row.find_elements(By.TAG_NAME, "td")

            for i, cell in enumerate(cells):
                if i < len(headers):  # Only map if there's a corresponding header
                    investor[headers[i]] = cell.text

            investors_data.append(investor)

        return investors_data
    except Exception as e:
        print(f"Error scraping Investors: {e}")
        return []

# Function to scrape Authorized Signatories
def scrape_signatories():
    try:
        # Click on the Authorized Signatories tab
        signatories_tab = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/div[2]/div[11]/div[1]/h2/a")))
        if "collapsed" in signatories_tab.get_attribute("class"):
            signatories_tab.click()  # Expand the tab
        time.sleep(1)  # Wait for the content to load

        # Extract the signatories table
        signatories_table = driver.find_element(By.CSS_SELECTOR, "#signatoriesSection > div > div > table")
        table_header = signatories_table.find_element(By.TAG_NAME, "thead")
        headers = [th.text for th in table_header.find_elements(By.TAG_NAME, "th")]

        table_body = signatories_table.find_element(By.TAG_NAME, "tbody")
        rows = table_body.find_elements(By.TAG_NAME, "tr")

        signatories_data = []
        for row in rows:
            signatory = {}
            cells = row.find_elements(By.TAG_NAME, "td")

            for i, cell in enumerate(cells):
                if i < len(headers):  # Only map if there's a corresponding header
                    signatory[headers[i]] = cell.text

            signatories_data.append(signatory)

        return signatories_data
    except Exception as e:
        print(f"Error scraping Signatories: {e}")
        return []

# Function to scrape Auditor details
# def scrape_auditors():
#     try:
#         # Click on the Auditor tab
#         auditors_tab = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/div[2]/div[12]/div[1]/h2/a")))
#         if "collapsed" in auditors_tab.get_attribute("class"):
#             auditors_tab.click()  # Expand the tab
#         time.sleep(1)  # Wait for the content to load

#         # Extract the auditors table
#         auditors_table = driver.find_element(By.CSS_SELECTOR, "#auditorsSection > div > div > table")
#         table_header = auditors_table.find_element(By.TAG_NAME, "thead")
#         headers = [th.text for th in table_header.find_elements(By.TAG_NAME, "th")]

#         table_body = auditors_table.find_element(By.TAG_NAME, "tbody")
#         rows = table_body.find_elements(By.TAG_NAME, "tr")

#         auditors_data = []
#         for row in rows:
#             auditor = {}
#             cells = row.find_elements(By.TAG_NAME, "td")

#             for i, cell in enumerate(cells):
#                 if i < len(headers):  # Only map if there's a corresponding header
#                     auditor[headers[i]] = cell.text

#             auditors_data.append(auditor)

#         return auditors_data
#     except Exception as e:
#         print(f"Error scraping Auditors: {e}")
#         return []


def scrape_auditors():
    try:
        # Click on the Auditor tab
        auditors_tab = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/div[2]/div[12]/div[1]/h2/a")))
        if "collapsed" in auditors_tab.get_attribute("class"):
            auditors_tab.click()  # Expand the tab
        time.sleep(1)  # Wait for the content to load

        # Extract the auditors table
        auditors_table = driver.find_element(By.CSS_SELECTOR, "#auditorsSection > div > div > table")
        table_header = auditors_table.find_element(By.TAG_NAME, "thead")
        headers = [th.text for th in table_header.find_elements(By.TAG_NAME, "th")]

        table_body = auditors_table.find_element(By.TAG_NAME, "tbody")
        rows = table_body.find_elements(By.TAG_NAME, "tr")

        auditors_data = []
        for row in rows:
            auditor = {}
            cells = row.find_elements(By.TAG_NAME, "td")

            # Filter out empty rows (where cells are empty or invalid)
            if any(cell.text.strip() for cell in cells):  # Check if any cell has content
                for i, cell in enumerate(cells):
                    if i < len(headers):  # Only map if there's a corresponding header
                        auditor[headers[i]] = cell.text.strip()  # Clean up the text

                auditors_data.append(auditor)

        return auditors_data
    except Exception as e:
        print(f"Error scraping Auditors: {e}")
        return []

# Function to scrape Fiscal Information
# def scrape_fiscal_information():
#     try:
#         # Click on the Fiscal Information tab
#         fiscal_info_tab = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/div[2]/div[8]/div[1]/h2/a")))
#         if "collapsed" in fiscal_info_tab.get_attribute("class"):
#             fiscal_info_tab.click()  # Expand the tab
#         time.sleep(1)  # Wait for the content to load

#         # Extract the fiscal information
#         fiscal_info_section = driver.find_element(By.CSS_SELECTOR, "#fiscalInformationSection > div")
#         fiscal_info_details = {}

#         fiscal_info_details["CR Establishment Date"] = fiscal_info_section.find_element(By.CSS_SELECTOR, "div:nth-child(1) > div > div > div").text
#         fiscal_info_details["First Financial Year End"] = fiscal_info_section.find_element(By.CSS_SELECTOR, "div:nth-child(2) > div > div > div:nth-child(1)").text
#         fiscal_info_details["Fiscal Year End"] = fiscal_info_section.find_element(By.CSS_SELECTOR, "div:nth-child(2) > div > div > div:nth-child(2)").text

#         return fiscal_info_details
#     except Exception as e:
#         print(f"Error scraping Fiscal Information: {e}")
#         return {}
# Function to scrape Fiscal Information and clean up the extracted text
def scrape_fiscal_information():
    try:
        # Click on the Fiscal Information tab
        fiscal_info_tab = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/div[2]/div[8]/div[1]/h2/a")))
        if "collapsed" in fiscal_info_tab.get_attribute("class"):
            fiscal_info_tab.click()  # Expand the tab
        time.sleep(1)  # Wait for the content to load

        # Extract the fiscal information
        fiscal_info_section = driver.find_element(By.CSS_SELECTOR, "#fiscalInformationSection > div")
        fiscal_info_details = {}

        # Function to clean up text
        def clean_text(text):
            # Remove unwanted headers and extract only the date or relevant information
            cleaned_text = re.sub(r"CR Establishment Date|First Financial Year End|Fiscal Year End", "", text).strip()
            return cleaned_text

        fiscal_info_details["CR Establishment Date"] = clean_text(fiscal_info_section.find_element(By.CSS_SELECTOR, "div:nth-child(1) > div > div > div").text)
        fiscal_info_details["First Financial Year End"] = clean_text(fiscal_info_section.find_element(By.CSS_SELECTOR, "div:nth-child(2) > div > div > div:nth-child(1)").text)
        fiscal_info_details["Fiscal Year End"] = clean_text(fiscal_info_section.find_element(By.CSS_SELECTOR, "div:nth-child(2) > div > div > div:nth-child(2)").text)

        return fiscal_info_details
    except Exception as e:
        print(f"Error scraping Fiscal Information: {e}")
        return {}



# Scrape Commercial Name
commercial_name_details = scrape_tab(
    "/html/body/div[2]/div[2]/div[2]/div[2]/div[1]/h2/a",
    {
        "Arabic Name": "#commercialNameSection > div > div > div:nth-child(1) > div",
        "English Name": "#commercialNameSection > div > div > div:nth-child(2) > div"
    }
)
data["Commercial Name"].append(commercial_name_details)

# Scrape Legal Type
legal_type_details = scrape_tab(
    "/html/body/div[2]/div[2]/div[2]/div[3]/div[1]/h2/a",
    {
        "Legal Type": "#legalTypeSection > div > div > div > div"
    }
)
data["Legal Type"].append(legal_type_details)

# Scrape Registry Information
registry_info_details = scrape_tab(
    "/html/body/div[2]/div[2]/div[2]/div[4]/div[1]/h2/a",
    {
        "Commercial Registration No": "#registryInformationSection > div > div > div:nth-child(1) > div > p",
        "Registration Date": "#registryInformationSection > div > div > div:nth-child(2) > div > p",
        "Registration Status": "#registryInformationSection > div > div > div:nth-child(3) > div > p",
        "Expiry Date": "#registryInformationSection > div > div > div:nth-child(4) > div > p"
    }
)
data["Registry Information"].append(registry_info_details)

# Scrape Address
address_details = scrape_tab(
    "/html/body/div[2]/div[2]/div[2]/div[5]/div[1]/h2/a",
    {
        "Business Location": "#companyAddressSection > div > div > div:nth-child(1) > div > div",
        "Street Name English": "#companyAddressSection > div > div > div:nth-child(2) > div > div:nth-child(1) > div",
        "Street Name Arabic": "#companyAddressSection > div > div > div:nth-child(3) > div > div:nth-child(1) > div",
        "Way Number": "#companyAddressSection > div > div > div:nth-child(2) > div > div:nth-child(2) > div",
        "Postal Code": "#companyAddressSection > div > div > div:nth-child(3) > div > div:nth-child(2) > div",
        "Building Number": "#companyAddressSection > div > div > div:nth-child(2) > div > div:nth-child(3) > div",
        "P.O. Box": "#companyAddressSection > div > div > div:nth-child(3) > div > div:nth-child(3) > div",
        "Block Number": "#companyAddressSection > div > div > div:nth-child(2) > div > div:nth-child(4) > div",
        "Latitude": "#companyAddressSection > div > div > div:nth-child(3) > div > div:nth-child(4) > div > p",
        "Unit Number": "#companyAddressSection > div > div > div:nth-child(2) > div > div:nth-child(5) > div",
        "Longitude": "#companyAddressSection > div > div > div:nth-child(3) > div > div:nth-child(5) > div > p"
    }
)
data["Address"].append(address_details)

# Scrape Contact Information
contact_info_details = scrape_tab(
    "/html/body/div[2]/div[2]/div[2]/div[6]/div[1]/h2/a",
    {
        "E-mail": "#contactInformationSection > div > div > div:nth-child(1) > div:nth-child(1) > div",
        "Mobile Number": "#contactInformationSection > div > div > div:nth-child(1) > div:nth-child(2) > div"
    }
)
data["Contact Information"].append(contact_info_details)

# Scrape Capital
capital_details = scrape_tab(
    "/html/body/div[2]/div[2]/div[2]/div[7]/div[1]/h2/a",
    {
        "Cash Capital": "#capitalSection > div > div > div:nth-child(1) > div > div:nth-child(1) > div",
        "Asset Capital": "#capitalSection > div > div > div:nth-child(1) > div > div:nth-child(2) > div",
        "Total Capital": "#capitalSection > div > div > div:nth-child(1) > div > div:nth-child(3) > div",
        "Share Count": "#capitalSection > div > div > div:nth-child(2) > div > div:nth-child(1) > div",
        "Share Value": "#capitalSection > div > div > div:nth-child(2) > div > div:nth-child(2) > div"
    }
)
data["Capital"].append(capital_details)

# Scrape Fiscal Information
# fiscal_info_details = scrape_tab(
#     "/html/body/div[2]/div[2]/div[2]/div[8]/div[1]/h2/a",
#     {
#         "CR Establishment Date": "#fiscalInformationSection > div > div > div:nth-child(1) > div > div > div",
#         "First Financial Year End": "#fiscalInformationSection > div > div > div:nth-child(2) > div > div > div:nth-child(1)",
#         "Fiscal Year End": "#fiscalInformationSection > div > div > div:nth-child(2) > div > div > div:nth-child(2)"
#     }
# )
# data["Fiscal Information"].append(fiscal_info_details)

# Call the function and save the data
fiscal_info_details = scrape_fiscal_information()
# Add to main data structure
data["Fiscal Information"].append(fiscal_info_details)

# Scrape Business Activities
# business_activities_details = scrape_tab(
#     "/html/body/div[2]/div[2]/div[2]/div[9]/div[1]/h2/a",
#     {
#         "Activities": "#declaredActivitiesSection > div > div > table > tbody"
#     }
# )
# data["Business Activities"].append(business_activities_details)

# Call the function and save the data
business_activities_details = scrape_business_activities()
# Add to main data structure
data["Business Activities"].append(business_activities_details)

# Scrape Investors
# investors_details = scrape_tab(
#     "/html/body/div[2]/div[2]/div[2]/div[10]/div[1]/h2/a",
#     {
#         "Investors": "#investorsSection > div > div > table > tbody"
#     }
# )
# data["Investors"].append(investors_details)


# Call the function and save the data
investors_details = scrape_investors()
# Add to main data structure
data["Investors"].append(investors_details)

# Scrape Authorized Signatories
# signatories_details = scrape_tab(
#     "/html/body/div[2]/div[2]/div[2]/div[11]/div[1]/h2/a",
#     {
#         "Signatories": "#signatoriesSection > div > div > table > tbody"
#     }
# )
# data["Authorized Signatories"].append(signatories_details)

# Call the function and save the data
signatories_details = scrape_signatories()
# Add to main data structure
data["Authorized Signatories"].append(signatories_details)

# Scrape Auditor
# auditor_details = scrape_tab(
#     "/html/body/div[2]/div[2]/div[2]/div[12]/div[1]/h2/a",
#     {
#         "Auditors": "#auditorsSection > div > div > table > tbody"
#     }
# )
# data["Auditor"].append(auditor_details)



# Call the function and save the data
auditor_details = scrape_auditors()
# Add to main data structure
data["Auditor"].append(auditor_details)

# Scrape Licenses
# licenses_details = scrape_tab(
#     "/html/body/div[2]/div[2]/div[2]/div[13]/div[1]/h2/a",
#     {
#         "Licenses": "#licenseSection > div > table > tbody"
#     }
# )
# data["Licenses"].append(licenses_details)
# Now, update the Licenses data collection to use this function
licenses_details = scrape_licenses()
data["Licenses"].append(licenses_details)
# Save data to JSON file
with open(os.path.join(output_dir, 'scraped_data.json'), 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=4)

# Clean Up
driver.quit()
print("Scraping completed and data saved.")