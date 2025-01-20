# import json
# import os
# import time
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, NoSuchElementException


# # Create directory for output files
# output_dir = 'Bank_details_lastly'
# os.makedirs(output_dir, exist_ok=True)

# def save_to_file(data, filename):
#     """Save data to a file"""
#     try:
#         filepath = os.path.join(output_dir, filename)
#         with open(filepath, 'w', encoding='utf-8') as f:
#             if isinstance(data, (dict, list)):
#                 json.dump(data, f, ensure_ascii=False, indent=4)
#             else:
#                 f.write(str(data))
#         print(f"Successfully saved {filename}")
#     except Exception as e:
#         print(f"Error saving {filename}: {e}")

# def scrape_table_section(table_selector, driver):
#     """Scrape table content"""
#     try:
#         table = driver.find_element(By.CSS_SELECTOR, table_selector)
#         headers = [th.text.strip() for th in table.find_elements(By.CSS_SELECTOR, "thead th")]
#         rows = []
        
#         for row in table.find_elements(By.CSS_SELECTOR, "tbody tr"):
#             cells = row.find_elements(By.TAG_NAME, "td")
#             row_data = {}
#             for i, cell in enumerate(cells):
#                 if i < len(headers):
#                     row_data[headers[i]] = cell.text.strip()
#             if row_data:
#                 rows.append(row_data)
        
#         return rows
#     except Exception as e:
#         print(f"Error scraping table {table_selector}: {e}")
#         return []

# def scrape_accordion_section(accordion_selector, detailed_section_selector, driver):
#     """Scrape accordion-style section where rows need to be clicked to expand for more details"""
#     data = []
#     rows = driver.find_elements(By.CSS_SELECTOR, accordion_selector)
    
#     for index, row in enumerate(rows):
#         try:
#             # Click the row to expand
#             row.click()
            
#             # Wait for the details to load
#             WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.CSS_SELECTOR, detailed_section_selector.format(index)))
#             )
            
#             # Scrape the detailed section
#             details_section = driver.find_element(By.CSS_SELECTOR, detailed_section_selector.format(index))
#             row_data = {
#                 "Name": details_section.find_element(By.CSS_SELECTOR, ".name-selector").text.strip(),
#                 "Details": details_section.find_element(By.CSS_SELECTOR, ".details-selector").text.strip(),
#             }
#             data.append(row_data)
#         except Exception as e:
#             print(f"Error processing row {index}: {e}")
    
#     return data

# def scrape_business_activities(driver):
#     """Scrape Business Activities tab"""
#     try:
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div[2]/div[dynamic value]/div[1]/h2/a")))
#         activities_data = scrape_table_section("#declaredActivitiesSection > div > div > table", driver)
#         if activities_data:
#             save_to_file(activities_data, "business_activities.txt")
#     except Exception as e:
#         print(f"Error scraping Business Activities: {e}")

# def scrape_investors(driver):
#     """Scrape Investors tab"""
#     try:
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div[2]/div[dynamic value]/div[1]/h2/a")))
#         investor_data = scrape_accordion_section("#investorsSection > div > div > table > tbody > tr.accordion-toggle.tr-collapse.collapsed", "#row_id__investors_{}", driver)
#         if investor_data:
#             save_to_file(investor_data, "investor_details.txt")
#     except Exception as e:
#         print(f"Error scraping Investors: {e}")

# def scrape_signatories(driver):
#     """Scrape Authorized Signatories tab"""
#     try:
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div[2]/div[dynamic value]/div[1]/h2/a")))
#         signatory_data = scrape_accordion_section("#signatoriesSection > div > div > table > tbody > tr.accordion-toggle.tr-collapse.collapsed", "#row_id__signatories_{}", driver)
#         if signatory_data:
#             save_to_file(signatory_data, "signatory_details.txt")
#     except Exception as e:
#         print(f"Error scraping Authorized Signatories: {e}")

# def scrape_auditors(driver):
#     """Scrape Auditors tab"""
#     try:
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div[2]/div[dynamic value]/div[1]/h2/a")))
#         auditor_data = scrape_accordion_section("#auditorsSection > div > div > table > tbody > tr.accordion-toggle.tr-collapse.collapsed", "#row_id__auditors_{}", driver)
#         if auditor_data:
#             save_to_file(auditor_data, "auditor_details.txt")
#     except Exception as e:
#         print(f"Error scraping Auditors: {e}")

# def scrape_licenses(driver):
#     """Scrape Licenses tab"""
#     try:
#         WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#content > div:nth-child(dynamic_value) > div.panel-heading > h2 > a")))
#         license_data = scrape_table_section("#licenseSection > div > table", driver)
#         if license_data:
#             save_to_file(license_data, "licenses.txt")
#     except Exception as e:
#         print(f"Error scraping Licenses: {e}")

# def main():
#     driver = webdriver.Chrome()
#     driver.maximize_window()
    
#     try:
#         # Initialize and navigate to the target URL
#         driver.get("https://www.business.gov.om/portal/searchEstablishments")
        
#         # Language selection (if needed)
#         language_selector = "#header > div > div > div.submenu-line.pull-right > div > a"
#         WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, language_selector))).click()
        
#         # Search for the bank
#         search_input = driver.find_element(By.ID, "search_company_name")
#         search_input.send_keys("بنك الاسكان العماني")
#         time.sleep(10)  # Wait for captcha
        
#         search_button = driver.find_element(By.CSS_SELECTOR, "#searchCompanyForm > div > div.row > div:nth-child(5) > button")
#         search_button.click()
        
#         # Wait for results and click the "View" link
#         WebDriverWait(driver, 20).until(
#             EC.presence_of_element_located((By.XPATH, "//table"))
#         )
        
#         results_table = driver.find_element(By.XPATH, "//table")
#         for row in results_table.find_elements(By.TAG_NAME, "tr"):
#             if "بنك الاسكان العماني" in row.text:
#                 row.find_element(By.LINK_TEXT, "View").click()
#                 break
        
#         time.sleep(2)  # Wait for details to load
        
#         # Scrape various tabs
#         scrape_business_activities(driver)
#         scrape_investors(driver)
#         scrape_signatories(driver)
#         scrape_auditors(driver)
#         scrape_licenses(driver)
        
#     finally:
#         driver.quit()

# if __name__ == "__main__":
#     main()




import time
import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Create directory for output files
output_dir = 'Bank_details_lasttime'
os.makedirs(output_dir, exist_ok=True)

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

def wait_for_element(driver, selector, by=By.CSS_SELECTOR, timeout=10):
    """Wait for an element to be visible and return it"""
    try:
        WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((by, selector))
        )
        return driver.find_element(by, selector)
    except Exception as e:
        print(f"Error waiting for element {selector}: {e}")
        return None

def scrape_section(driver, section_selector, file_name):
    """Scrape general sections and save them"""
    data = {}
    try:
        section = wait_for_element(driver, section_selector, By.CSS_SELECTOR)
        if section:
            rows = section.find_elements(By.CSS_SELECTOR, "div > div")  # You can adjust this selector based on structure
            for row in rows:
                header = row.find_element(By.TAG_NAME, "h3").text.strip() if row.find_elements(By.TAG_NAME, "h3") else None
                content = row.text.strip()
                if header:
                    data[header] = content
            if data:
                save_to_file(data, file_name)
    except Exception as e:
        print(f"Error scraping section {section_selector}: {e}")

def scrape_table_section(driver, table_selector):
    """Scrape table content"""
    try:
        table = wait_for_element(driver, table_selector, By.CSS_SELECTOR)
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
        print(f"Error scraping table {table_selector}: {e}")
        return []

def scrape_accordion_section(driver, accordion_selector, detailed_section_selector):
    """Scrape accordion-style section where rows need to be clicked to expand for more details"""
    data = []
    rows = driver.find_elements(By.CSS_SELECTOR, accordion_selector)
    
    for index, row in enumerate(rows):
        try:
            # Click the row to expand
            row.click()
            
            # Wait for the details to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, detailed_section_selector.format(index)))
            )
            
            # Scrape the detailed section
            details_section = driver.find_element(By.CSS_SELECTOR, detailed_section_selector.format(index))
            row_data = {
                "Name": details_section.find_element(By.CSS_SELECTOR, ".name-selector").text.strip(),
                "Details": details_section.find_element(By.CSS_SELECTOR, ".details-selector").text.strip(),
            }
            data.append(row_data)
        except Exception as e:
            print(f"Error processing row {index}: {e}")
    
    return data

def scrape_business_activities(driver):
    """Scrape Business Activities tab"""
    try:
        activity_tab_xpath = "/html/body/div[2]/div[2]/div[2]/div[dynamic value]/div[1]/h2/a"
        activity_tab = wait_for_element(driver, activity_tab_xpath, By.XPATH)
        
        if activity_tab:
            activity_tab.click()
            time.sleep(2)  # Allow the tab content to load
            
            # Scrape the table content
            activities_data = scrape_table_section(driver, "#declaredActivitiesSection > div > div > table")
            if activities_data:
                save_to_file(activities_data, "business_activities.txt")
        else:
            print("Business Activities tab not found.")
    except Exception as e:
        print(f"Error scraping Business Activities: {e}")

def scrape_investors(driver):
    """Scrape Investors tab"""
    try:
        investor_tab_xpath = "/html/body/div[2]/div[2]/div[2]/div[dynamic value]/div[1]/h2/a"
        investor_tab = wait_for_element(driver, investor_tab_xpath, By.XPATH)
        
        if investor_tab:
            investor_tab.click()
            time.sleep(2)  # Allow the tab content to load
            
            investor_data = scrape_accordion_section(driver, "#investorsSection > div > div > table > tbody > tr.accordion-toggle.tr-collapse.collapsed", "#row_id__investors_")
            if investor_data:
                save_to_file(investor_data, "investor_details.txt")
        else:
            print("Investors tab not found.")
    except Exception as e:
        print(f"Error scraping Investors: {e}")

def scrape_signatories(driver):
    """Scrape Authorized Signatories tab"""
    try:
        signatory_tab_xpath = "/html/body/div[2]/div[2]/div[2]/div[dynamic value]/div[1]/h2/a"
        signatory_tab = wait_for_element(driver, signatory_tab_xpath, By.XPATH)
        
        if signatory_tab:
            signatory_tab.click()
            time.sleep(2)  # Allow the tab content to load
            
            signatory_data = scrape_accordion_section(driver, "#signatoriesSection > div > div > table > tbody > tr.accordion-toggle.tr-collapse.collapsed", "#row_id__signatories_")
            if signatory_data:
                save_to_file(signatory_data, "signatory_details.txt")
        else:
            print("Authorized Signatories tab not found.")
    except Exception as e:
        print(f"Error scraping Authorized Signatories: {e}")

def scrape_auditors(driver):
    """Scrape Auditors tab"""
    try:
        auditor_tab_xpath = "/html/body/div[2]/div[2]/div[2]/div[dynamic value]/div[1]/h2/a"
        auditor_tab = wait_for_element(driver, auditor_tab_xpath, By.XPATH)
        
        if auditor_tab:
            auditor_tab.click()
            time.sleep(2)  # Allow the tab content to load
            
            auditor_data = scrape_accordion_section(driver, "#auditorsSection > div > div > table > tbody > tr.accordion-toggle.tr-collapse.collapsed", "#row_id__auditors_")
            if auditor_data:
                save_to_file(auditor_data, "auditor_details.txt")
        else:
            print("Auditors tab not found.")
    except Exception as e:
        print(f"Error scraping Auditors: {e}")

def scrape_licenses(driver):
    """Scrape Licenses tab"""
    try:
        license_tab_xpath = "/html/body/div[2]/div[2]/div[2]/div[12]/div[2]/div/table/tbody"
        license_tab = wait_for_element(driver, license_tab_xpath, By.XPATH)
        
        if license_tab:
            license_data = scrape_table_section(driver, "#licenseSection > div > table")
            if license_data:
                save_to_file(license_data, "licenses.txt")
        else:
            print("Licenses tab not found.")
    except Exception as e:
        print(f"Error scraping Licenses: {e}")

def scrape_commercial_name(driver):
    """Scrape Commercial Name"""
    try:
        scrape_section(driver, "#commercialNameSection", "commercial_name.txt")
    except Exception as e:
        print(f"Error scraping Commercial Name: {e}")

def scrape_legal_type(driver):
    """Scrape Legal Type"""
    try:
        scrape_section(driver, "#legalTypeSection", "legal_type.txt")
    except Exception as e:
        print(f"Error scraping Legal Type: {e}")

def scrape_registry_information(driver):
    """Scrape Registry Information"""
    try:
        scrape_section(driver, "#registryInfoSection", "registry_info.txt")
    except Exception as e:
        print(f"Error scraping Registry Information: {e}")

def scrape_address(driver):
    """Scrape Address"""
    try:
        scrape_section(driver, "#addressSection", "address.txt")
    except Exception as e:
        print(f"Error scraping Address: {e}")

def scrape_contact_information(driver):
    """Scrape Contact Information"""
    try:
        scrape_section(driver, "#contactInfoSection", "contact_info.txt")
    except Exception as e:
        print(f"Error scraping Contact Information: {e}")

def scrape_capital(driver):
    """Scrape Capital"""
    try:
        scrape_section(driver, "#capitalSection", "capital.txt")
    except Exception as e:
        print(f"Error scraping Capital: {e}")

def scrape_fiscal_information(driver):
    """Scrape Fiscal Information"""
    try:
        scrape_section(driver, "#fiscalInfoSection", "fiscal_info.txt")
    except Exception as e:
        print(f"Error scraping Fiscal Information: {e}")

def main():
    driver = webdriver.Chrome()
    driver.maximize_window()
    
    try:
        # Initialize and navigate to the target URL
        driver.get("https://www.business.gov.om/portal/searchEstablishments")
        
        # Language selection (if needed)
        language_selector = "#header > div > div > div.submenu-line.pull-right > div > a"
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, language_selector))).click()
        
        # Search for the bank
        search_input = driver.find_element(By.ID, "search_company_name")
        search_input.send_keys("بنك الاسكان العماني")
        time.sleep(10)  # Wait for captcha
        
        search_button = driver.find_element(By.CSS_SELECTOR, "#searchCompanyForm > div > div.row > div:nth-child(5) > button")
        search_button.click()
        
        # Wait for results and click the "View" link
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//table"))
        )
        
        results_table = driver.find_element(By.XPATH, "//table")
        for row in results_table.find_elements(By.TAG_NAME, "tr"):
            if "بنك الاسكان العماني" in row.text:
                row.find_element(By.LINK_TEXT, "View").click()
                break
        
        time.sleep(2)  # Wait for details to load
        
        # Scrape all sections
        scrape_commercial_name(driver)
        scrape_legal_type(driver)
        scrape_registry_information(driver)
        scrape_address(driver)
        scrape_contact_information(driver)
        scrape_capital(driver)
        scrape_fiscal_information(driver)
        
        # Scrape tabs
        scrape_business_activities(driver)
        scrape_investors(driver)
        scrape_signatories(driver)
        scrape_auditors(driver)
        scrape_licenses(driver)
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
