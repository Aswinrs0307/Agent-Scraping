import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


url="https://efiling.drcor.mcit.gov.cy/DrcorPublic/SearchForm.aspx?sc=0&cultureInfo=en-AU"
name="BANK OF CYPRUS PUBLIC COMPANY LIMITED"

# Create directory for output files
Company_name = "".join(c if c.isalnum() or c.isspace() else "_" for c in name).strip()
output_dir = Company_name
os.makedirs(output_dir, exist_ok=True)

# Initialize the Selenium WebDriver
driver = webdriver.Chrome()  # or use webdriver.Firefox() or any other browser
driver.get(url)

# Perform search
search_input = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucSearch_txtName")
search_input.send_keys(name)
search_button = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucSearch_lbtnSearch")
search_button.click()

# Wait for results to load
wait = WebDriverWait(driver, 10)  # Wait for up to 10 seconds

# Navigate to Results
results_table = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/form/div[3]/div[3]/table/tbody/tr/td/table/tbody/tr[9]/td/div/table")))
rows = results_table.find_elements(By.CLASS_NAME, "basket")

# Find the correct entry
row_number = None
for index, row in enumerate(rows):
    if "Select" in row.get_attribute("onclick"):
        if name in row.text:
            row_number = index
            break

if row_number is not None:
    # Trigger the onclick attribute to navigate to the organization details page
    driver.execute_script(f"__doPostBack('ctl00$cphMyMasterCentral$GridView1','Select${row_number}')")
else:
    print("No matching row found.")
    driver.quit()
    exit()

# Scrape Organization details
time.sleep(5)  # Wait for the details to load
organization_details = {}
organization_details['Name'] = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblName").text
organization_details['Registration Number'] = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblNumber").text  
organization_details['Type'] = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblType").text
organization_details['SubType'] = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblSubType").text
organization_details['Name Status'] = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblNameStatus").text      
organization_details['Registration Date'] = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblRegistrationDate").text
organization_details['Organization Status'] = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblStatus").text  
organization_details['Country of Incorporation'] = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_trOrigingCountry").text
organization_details['Status Date'] = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblstatusDate").text      
organization_details['Last Annual Return Date'] = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblLastAnnualReturnDate").text

# Save organization details
with open(os.path.join(output_dir, 'organization_details.txt'), 'w', encoding='utf-8') as f:
    for key, value in organization_details.items():
        f.write(f"{key}: {value}\n")

# Scrape File Status
file_status = {}
file_status['Last File Update'] = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_lblFileLastUpdateVal").text
file_status['Pending Services'] = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_lblFoundNo").text

# Save file status
with open(os.path.join(output_dir, 'file_status.txt'), 'w', encoding='utf-8') as f:
    for key, value in file_status.items():
        f.write(f"{key}: {value}\n")

# Scrape Additional Tables from File Status
additional_table_data = []
while True:
    try:
        additional_table = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/form/div[3]/div[3]/div[5]/div/div/div[4]/div[2]/div[1]/div[4]/div[2]/div/table")))
        rows = additional_table.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            additional_table_data.append([cell.text for cell in cells])

        # Check for pagination
        next_page_button = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_NextPage")
        if "disabled" in next_page_button.get_attribute("outerHTML"):
            break
        next_page_button.click()
        wait.until(EC.staleness_of(next_page_button))  # Wait for the page to refresh
    except Exception as e:
        print("Error while scraping additional tables:", e)
        break

# Save additional table data
with open(os.path.join(output_dir, 'additional_table.txt'), 'w', encoding='utf-8') as f:
    for row in additional_table_data:
        f.write("\t".join(row) + "\n")

# Scrape Directors and Secretaries
driver.find_element(By.ID, "ctl00_cphMyMasterCentral_directors").click()
time.sleep(5)  # Wait for the details to load
directors_data = []
directors_table = driver.find_element(By.XPATH, "/html/body/form/div[3]/div[3]/div[5]/div/div/div[4]/div[2]/div[2]/div/div/table")
rows = directors_table.find_elements(By.TAG_NAME, "tr")
for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    directors_data.append([cell.text for cell in cells])

# Save directors and secretaries data
with open(os.path.join(output_dir, 'directors_secretaries.txt'), 'w', encoding='utf-8') as f:
    for row in directors_data:
        f.write("\t".join(row) + "\n")

# Scrape Registered Office
driver.find_element(By.ID, "registeredOffice").click()
time.sleep(5)  # Wait for the details to load
registered_office = {}
registered_office['Address Title'] = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_addressTitle").text
registered_office['Street Name'] = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_Street").text
registered_office['Parish'] = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_Parish").text
registered_office['Territory'] = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_Teritory").text

# Save registered office data
with open(os.path.join(output_dir, 'registered_office.txt'), 'w', encoding='utf-8') as f:
    for key, value in registered_office.items():
        f.write(f"{key}: {value}\n")

# Scrape HE32 Archive
driver.find_element(By.ID, "HE32Archive").click()
time.sleep(5)  # Wait for the details to load
he32_archive_data = []
he32_table = driver.find_element(By.XPATH, "/html/body/form/div[3]/div[3]/div[5]/div/div/div[4]/div[2]/div[4]/div/div/table")
rows = he32_table.find_elements(By.TAG_NAME, "tr")
for row in rows:
    cells = row.find_elements(By.TAG_NAME, "td")
    he32_archive_data.append([cell.text for cell in cells])

# Save HE32 archive data
with open(os.path.join(output_dir, 'he32_archive.txt'), 'w', encoding='utf-8') as f:
    for row in he32_archive_data:
        f.write("\t".join(row) + "\n")

# Initialize variables
preview_files_data = []

# Scrape Preview Files Documents
driver.find_element(By.ID, "ctl00_cphMyMasterCentral_lbtnPreviewFileDocuments").click()
time.sleep(2)  # Wait for the page to load
driver.find_element(By.ID, "ctl00_cphMyMasterCentral_rdFileType_0").click()
time.sleep(2)  # Wait for the page to load
preview_files = []
while True:
    table = driver.find_element(By.XPATH, "/html/body/form/div[3]/div[3]/div[5]/div/div[2]/div/div/table")
    rows = table.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        preview_files.append([cell.text for cell in row.find_elements(By.TAG_NAME, "td")])

    try:
        next_button = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_NextPage")
        if "disabled" in next_button.get_attribute("outerHTML"):
            break
        next_button.click()
        time.sleep(2)  # Wait for the next page to load
    except Exception as e:
        print("Error navigating to next page:", e)
        break

# Save preview files
with open(os.path.join(output_dir, 'File_Documents_main.txt'), 'w', encoding='utf-8') as f:
    for entry in preview_files:
        f.write(', '.join(entry) + '\n')

# Scrape Charges and Mortgages
try:
    driver.find_element(By.ID, "ctl00_cphMyMasterCentral_rdFileType_1").click()
    time.sleep(2)  # Wait for the page to load
    charges_mortgages = []
    while True:
        table = driver.find_element(By.XPATH, "/html/body/form/div[3]/div[3]/div[5]/div/div[2]/div/div/table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            charges_mortgages.append([cell.text for cell in row.find_elements(By.TAG_NAME, "td")])

        try:
            next_button = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_NextPage")
            if "disabled" in next_button.get_attribute("outerHTML"):
                break
            next_button.click()
            time.sleep(2)  # Wait for the next page to load
        except Exception as e:
            print("Error navigating to next page:", e)
            break

    # Save charges and mortgages
    with open(os.path.join(output_dir, 'File_Documents_Chargesndmontages.txt'), 'w', encoding='utf-8') as f:
        for entry in charges_mortgages:
            f.write(', '.join(entry) + '\n')

except Exception as e:
    print("No records found for Charges and Mortgages:", e)

# Scrape Translations
try:
    driver.find_element(By.ID, "ctl00_cphMyMasterCentral_rdFileType_2").click()
    time.sleep(2)  # Wait for the page to load
    translations = []
    while True:
        table = driver.find_element(By.XPATH, "/html/body/form/div[3]/div[3]/div[5]/div/div[2]/div/div/table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            translations.append([cell.text for cell in row.find_elements(By.TAG_NAME, "td")])

        try:
            next_button = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_NextPage")
            if "disabled" in next_button.get_attribute("outerHTML"):
                break
            next_button.click()
            time.sleep(2)  # Wait for the next page to load
        except Exception as e:
            print("Error navigating to next page:", e)
            break

    # Save translations
    with open(os.path.join(output_dir, 'File_Documents_Translation.txt'), 'w', encoding='utf-8') as f:
        for entry in translations:
            f.write(', '.join(entry) + '\n')

except Exception as e:
    print("No records found for Translations:", e)

# Compile all data into JSON format
output_data = {
    "Organization details": organization_details,
    "File Status": file_status,
    "Additional Tables": additional_table_data,
    "Directors and Secretaries": directors_data,
    "HE32 Archive": he32_archive_data,
    "Registered Office": registered_office,
    "Preview File Type": preview_files,
    "Charges and Mortgages": charges_mortgages,
    "Translations": translations
}

# Save JSON output
with open(os.path.join(output_dir, 'output.json'), 'w', encoding='utf-8') as json_file:
    json.dump(output_data, json_file, ensure_ascii=False, indent=4)

# Clean Up
driver.quit()