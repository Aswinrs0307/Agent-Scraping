# import json
# import sys
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, NoSuchElementException
# import os
# import time

# # Create directory for output files
# output_dir = 'Bank_details'
# os.makedirs(output_dir, exist_ok=True)

# # Initialize the Selenium web driver
# driver = webdriver.Chrome()
# driver.maximize_window()  # Maximize window to ensure all elements are visible
# driver.get("https://www.business.gov.om/portal/searchEstablishments")

# # Language selection
# language_selector = "#header > div > div > div.submenu-line.pull-right > div > a"
# WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, language_selector))).click()

# # Perform search
# search_input = driver.find_element(By.ID, "search_company_name")
# search_input.send_keys("بنك الاسكان العماني")

# # Handle Captcha
# time.sleep(10)  # Wait for human interaction

# # Submit Search
# search_button = driver.find_element(By.CSS_SELECTOR, "#searchCompanyForm > div > div.row > div:nth-child(5) > button")
# search_button.click()

# # Wait for result to load
# # Wait for result to load
# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div/div/div/table")))

# # Navigate to Results
# results_table = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div/div/table")
# rows = results_table.find_elements(By.TAG_NAME, "tr")

# # Check for exact match
# exact_match_found = False
# for row in rows:
#     if "بنك الاسكان العماني" in row.text:
#         view_button = row.find_element(By.LINK_TEXT, "View")
#         view_button.click()
#         exact_match_found = True
#         break

# # Pagination handling if no exact match found
# if not exact_match_found:
#     while True:
#         pagination = driver.find_elements(By.XPATH, "/html/body/div[2]/div[2]/div/div/div/ul")
#         if pagination:
#             next_page = pagination[0].find_element(By.LINK_TEXT, "Next")
#             if next_page.get_attribute("href") != "#":
#                 next_page.click()
#                 time.sleep(2)  # Wait for the page to load
#                 rows = driver.find_elements(By.XPATH, "/html/body/div[2]/div[2]/div/div/div/table/tr")
#                 for row in rows:
#                     if "بنك الاسكان العماني" in row.text:
#                         view_button = row.find_element(By.LINK_TEXT, "View")
#                         view_button.click()
#                         exact_match_found = True
#                         break
#             else:
#                 break
#         else:
#             break

# # Function to scrape basic information
# def scrape_basic_info(section_id, section_name):
#     try:
#         elements = driver.find_elements(By.CSS_SELECTOR, f"#{section_id} .row > div")
#         info = {}
#         for element in elements:
#             try:
#                 label = element.find_element(By.CSS_SELECTOR, "label").text.strip()
#                 value = element.find_element(By.CSS_SELECTOR, "div, p").text.strip()
#                 info[label] = value
#             except NoSuchElementException:
#                 continue
#         return info
#     except Exception as e:
#         print(f"Error scraping {section_name}: {e}")
#         return {}

# # Function to scrape table data
# def scrape_table_data(table_id):
#     try:
#         # Get headers
#         headers = []
#         header_elements = driver.find_elements(By.CSS_SELECTOR, f"#{table_id} thead th")
#         for header in header_elements:
#             headers.append(header.text.strip())
        
#         # Get rows
#         rows = []
#         row_elements = driver.find_elements(By.CSS_SELECTOR, f"#{table_id} tbody tr")
#         for row in row_elements:
#             cell_elements = row.find_elements(By.TAG_NAME, "td")
#             row_data = {}
#             for i, cell in enumerate(cell_elements):
#                 if i < len(headers):
#                     row_data[headers[i]] = cell.text.strip()
#             rows.append(row_data)
        
#         return rows
#     except Exception as e:
#         print(f"Error scraping table {table_id}: {e}")
#         return []

# # Function to scrape expandable rows
# def scrape_expandable_rows(section_id):
#     try:
#         rows = []
#         expandable_rows = driver.find_elements(By.CSS_SELECTOR, f"#{section_id} tbody tr.accordion-toggle")
        
#         for index, row in enumerate(expandable_rows):
#             try:
#                 # Get initial row data
#                 cells = row.find_elements(By.TAG_NAME, "td")
#                 row_data = {
#                     "index": index,
#                     "main_info": {cell.text.strip() for cell in cells if cell.text.strip()}
#                 }
                
#                 # Click to expand
#                 row.click()
#                 time.sleep(1)  # Wait for expansion
                
#                 # Get expanded content
#                 expanded_id = f"row_id__{section_id}_{index}"
#                 expanded_section = WebDriverWait(driver, 5).until(
#                     EC.presence_of_element_located((By.ID, expanded_id))
#                 )
                
#                 # Get all details from expanded section
#                 details = {}
#                 detail_rows = expanded_section.find_elements(By.CSS_SELECTOR, ".row > div")
#                 for detail in detail_rows:
#                     try:
#                         label = detail.find_element(By.TAG_NAME, "label").text.strip()
#                         value = detail.find_element(By.CSS_SELECTOR, "div, p").text.strip()
#                         details[label] = value
#                     except NoSuchElementException:
#                         continue
                
#                 row_data["details"] = details
#                 rows.append(row_data)
                
#                 # Collapse row
#                 row.click()
#                 time.sleep(0.5)
                
#             except Exception as row_error:
#                 print(f"Error processing row {index}: {row_error}")
#                 continue
                
#         return rows
#     except Exception as e:
#         print(f"Error scraping expandable section {section_id}: {e}")
#         return []

# # Initialize data dictionary
# data = {}

# # Commercial Name
# tab = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'commercialNameSection')]"))
# )
# tab.click()
# data["Commercial Name"] = scrape_basic_info("commercialNameSection", "Commercial Name")

# # Legal Type
# tab = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'legalTypeSection')]"))
# )
# tab.click()
# data["Legal Type"] = scrape_basic_info("legalTypeSection", "Legal Type")

# # Registry Information
# tab = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'registryInformationSection')]"))
# )
# tab.click()
# data["Registry Information"] = scrape_basic_info("registryInformationSection", "Registry Information")

# # Address
# tab = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'companyAddressSection')]"))
# )
# tab.click()
# data["Address"] = scrape_basic_info("companyAddressSection", "Address")

# # Contact Information
# tab = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'contactInformationSection')]"))
# )
# tab.click()
# data["Contact Information"] = scrape_basic_info("contactInformationSection", "Contact Information")

# # Capital
# tab = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'capitalSection')]"))
# )
# tab.click()
# data["Capital"] = scrape_basic_info("capitalSection", "Capital")

# # Fiscal Information
# tab = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'fiscalInformationSection')]"))
# )
# tab.click()
# data["Fiscal Information"] = scrape_basic_info("fiscalInformationSection", "Fiscal Information")

# # Business Activities
# tab = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'declaredActivitiesSection')]"))
# )
# tab.click()
# data["Business Activities"] = scrape_table_data("declaredActivitiesTable")

# # Investors
# try:
#     tab = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'investorsSection')]"))
#     )
#     tab.click()
#     time.sleep(1)
#     data["Investors"] = scrape_expandable_rows("investors")
# except TimeoutException:
#     print("Investors tab not found")
#     data["Investors"] = []

# # Authorized Signatories
# try:
#     tab = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'signatoriesSection')]"))
#     )
#     tab.click()
#     time.sleep(1)
#     data["Authorized Signatories"] = scrape_expandable_rows("signatories")
# except TimeoutException:
#     print("Authorized Signatories tab not found")
#     data["Authorized Signatories"] = []

# # Auditor
# try:
#     tab = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'auditorsSection')]"))
#     )
#     tab.click()
#     time.sleep(1)
#     data["Auditor"] = scrape_expandable_rows("auditors")
# except TimeoutException:
#     print("Auditor tab not found")
#     data["Auditor"] = []

# # Licenses
# try:
#     tab = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, "//a[contains(@href,'licenseSection')]"))
#     )
#     tab.click()
#     time.sleep(1)
#     data["Licenses"] = scrape_table_data("licenseTable")
# except TimeoutException:
#     print("Licenses tab not found")
#     data["Licenses"] = []

# # Save complete data to JSON file
# with open(os.path.join(output_dir, 'output.json'), 'w', encoding='utf-8') as f:
#     json.dump(data, f, ensure_ascii=False, indent=4)

# # Save individual sections to separate files
# for section_name, section_data in data.items():
#     filename = f"{section_name.lower().replace(' ', '_')}.txt"
#     with open(os.path.join(output_dir, filename), 'w', encoding='utf-8') as f:
#         json.dump(section_data, f, ensure_ascii=False, indent=4)

# # Clean Up
# driver.quit()


import json
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
import time

# Create directory for output files
output_dir = 'Bank_details_again'
os.makedirs(output_dir, exist_ok=True)

def scrape_basic_section(section_id, driver):
    """Scrape basic section content without clicking the tab"""
    try:
        section = driver.find_element(By.ID, section_id)
        content = {}
        rows = section.find_elements(By.CSS_SELECTOR, ".row > div")
        
        for row in rows:
            try:
                label = row.find_element(By.CSS_SELECTOR, "label").text.strip()
                value = row.find_element(By.CSS_SELECTOR, "div:not(label)").text.strip()
                if label and value:
                    content[label] = value
            except NoSuchElementException:
                continue
        
        return content
    except Exception as e:
        print(f"Error scraping section {section_id}: {e}")
        return {}

def scrape_table_section(table_id, driver):
    """Scrape table content"""
    try:
        table = driver.find_element(By.ID, table_id)
        headers = [th.text.strip() for th in table.find_elements(By.CSS_SELECTOR, "thead th")]
        rows = []
        
        for row in table.find_elements(By.CSS_SELECTOR, "tbody tr"):
            cells = row.find_elements(By.TAG_NAME, "td")
            row_data = {}
            for i, cell in enumerate(cells):
                if i < len(headers):
                    row_data[headers[i]] = cell.text.strip()
            if row_data:
                rows.append(row_data)
        
        return rows
    except Exception as e:
        print(f"Error scraping table {table_id}: {e}")
        return []

def save_to_file(data, filename):
    """Save data to a file"""
    try:
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            if isinstance(data, (dict, list)):
                json.dump(data, f, ensure_ascii=False, indent=4)
            else:
                f.write(str(data))
        print(f"Successfully saved {filename}")
    except Exception as e:
        print(f"Error saving {filename}: {e}")

def main():
    driver = webdriver.Chrome()
    driver.maximize_window()
    all_data = {}
    
    try:
        # Initialize and navigate
        driver.get("https://www.business.gov.om/portal/searchEstablishments")
        
        # Language selection
        language_selector = "#header > div > div > div.submenu-line.pull-right > div > a"
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, language_selector))).click()
        
        # Search
        search_input = driver.find_element(By.ID, "search_company_name")
        search_input.send_keys("بنك الاسكان العماني")
        time.sleep(10)  # Wait for captcha
        
        search_button = driver.find_element(By.CSS_SELECTOR, "#searchCompanyForm > div > div.row > div:nth-child(5) > button")
        search_button.click()
        
        # Wait for results and click view
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//table"))
        )
        
        results_table = driver.find_element(By.XPATH, "//table")
        for row in results_table.find_elements(By.TAG_NAME, "tr"):
            if "بنك الاسكان العماني" in row.text:
                row.find_element(By.LINK_TEXT, "View").click()
                break
        
        time.sleep(2)  # Wait for details to load
        
        # Basic sections (Commercial Name to Fiscal Information)
        basic_sections = {
            "Commercial Name": "commercialNameSection",
            "Legal Type": "legalTypeSection",
            "Registry Information": "registryInformationSection",
            "Address": "companyAddressSection",
            "Contact Information": "contactInformationSection",
            "Capital": "capitalSection",
            "Fiscal Information": "fiscalInformationSection"
        }
        
        # Scrape basic sections
        for section_name, section_id in basic_sections.items():
            try:
                print(f"Scraping {section_name}...")
                data = scrape_basic_section(section_id, driver)
                if data:
                    all_data[section_name] = data
                    save_to_file(data, f"{section_name.lower().replace(' ', '_')}.txt")
            except Exception as e:
                print(f"Error processing {section_name}: {e}")
                continue
        
        # Business Activities
        try:
            activities_data = scrape_table_section("declaredActivitiesTable", driver)
            if activities_data:
                all_data["Business Activities"] = activities_data
                save_to_file(activities_data, "business_activities.txt")
        except Exception as e:
            print(f"Error processing Business Activities: {e}")
        
        # Variable sections (Investors to Licenses)
        variable_sections = [
            ("Investors", "investors"),
            ("Authorized Signatories", "signatories"),
            ("Auditors", "auditors"),
            ("Licenses", "licenseTable")
        ]
        
        for section_name, section_id in variable_sections:
            try:
                print(f"Checking for {section_name}...")
                # Check if section exists
                sections = driver.find_elements(By.ID, section_id)
                if sections:
                    if section_name == "Licenses":
                        data = scrape_table_section(section_id, driver)
                    else:
                        # For investors, signatories, and auditors
                        rows = driver.find_elements(By.CSS_SELECTOR, f"#{section_id} tbody tr")
                        data = []
                        for row in rows:
                            cells = row.find_elements(By.TAG_NAME, "td")
                            row_data = {f"Column_{i}": cell.text.strip() for i, cell in enumerate(cells) if cell.text.strip()}
                            if row_data:
                                data.append(row_data)
                    
                    if data:
                        all_data[section_name] = data
                        save_to_file(data, f"{section_name.lower().replace(' ', '_')}.txt")
            except Exception as e:
                print(f"Error processing {section_name}: {e}")
                continue
        
        # Save complete data
        save_to_file(all_data, "complete_data.json")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main()