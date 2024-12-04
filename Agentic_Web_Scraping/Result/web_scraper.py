# filename: web_scraper.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize the WebDriver
driver = webdriver.Chrome()  # Make sure you have the ChromeDriver installed and in your PATH
driver.get("https://efiling.drcor.mcit.gov.cy/DrcorPublic/SearchForm.aspx?sc=0&cultureInfo=en-AU")

# Perform Search
search_input = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucSearch_txtName")
search_input.send_keys("BANK OF CYPRUS PUBLIC COMPANY LIMITED")
search_button = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucSearch_lbtnSearch")
search_button.click()

# Wait for Results to Load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Select')]")))

# Navigate to Results
select_link = driver.find_element(By.XPATH, "//a[contains(text(), 'Select')]")
driver.execute_script("arguments[0].click();", select_link)

# Wait for Organization Details to Load
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "organizationDetailsTab")))

# Scrape Organization Details
organization_details = {
    "Name": driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblName").text,
    "Registration Number": driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblNumber").text,
    "Type": driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblType").text,
    "Subtype": driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblSubType").text,
    "Name Status": driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblNameStatus").text,
    "Registration Date": driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblRegistrationDate").text,
    "Organization Status": driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblStatus").text,
    "Status Date": driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblstatusDate").text,
    "Last Annual Return Date": driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblLastAnnualReturnDate").text,
}

# Save Organization Details
with open("organization_details.txt", "w", encoding='utf-8') as f:
    for key, value in organization_details.items():
        f.write(f"{key}: {value}\n")

# Scrape File Status
file_status = {
    "Last File Update": driver.find_element(By.ID, "ctl00_cphMyMasterCentral_lblFileLastUpdateVal").text,
    "Pending Services": driver.find_element(By.ID, "ctl00_cphMyMasterCentral_lblFoundNo").text,
}

# Save File Status
with open("file_status.txt", "w", encoding='utf-8') as f:
    for key, value in file_status.items():
        f.write(f"{key}: {value}\n")

# Scrape Additional Tables
additional_table_data = driver.find_element(By.XPATH, "/html/body/form/div[3]/div[3]/div[5]/div/div/div[4]/div[2]/div[1]/div[4]/div[2]/div/table").text
with open("additional_table.txt", "w", encoding='utf-8') as f:
    f.write(additional_table_data)

# Scrape Directors and Secretaries
directors_link = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_directors")
directors_link.click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ctl00_cphMyMasterCentral_OfficialsGrid")))
directors_data = driver.find_element(By.XPATH, "/html/body/form/div[3]/div[3]/div[5]/div/div/div[4]/div[2]/div[2]/div/div/table").text
with open("directors_secretaries.txt", "w", encoding='utf-8') as f:
    f.write(directors_data)

# Scrape Registered Office
registered_office_link = driver.find_element(By.ID, "registeredOffice")
registered_office_link.click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ctl00_cphMyMasterCentral_addressTitle")))
registered_office_data = {
    "Address Title": driver.find_element(By.ID, "ctl00_cphMyMasterCentral_addressTitle").text,
    "Street Name": driver.find_element(By.ID, "ctl00_cphMyMasterCentral_Street").text,
    "Parish": driver.find_element(By.ID, "ctl00_cphMyMasterCentral_Parish").text,
    "Territory": driver.find_element(By.ID, "ctl00_cphMyMasterCentral_Teritory").text,
}

# Save Registered Office
with open("registered_office.txt", "w", encoding='utf-8') as f:
    for key, value in registered_office_data.items():
        f.write(f"{key}: {value}\n")

# Scrape HE32 Archive
he32_archive_link = driver.find_element(By.ID, "HE32Archive")
he32_archive_link.click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ctl00_cphMyMasterCentral_gridHE32Archive")))
he32_archive_data = driver.find_element(By.XPATH, "/html/body/form/div[3]/div[3]/div[5]/div/div/div[4]/div[2]/div[4]/div/div/table").text
with open("he32_archive.txt", "w", encoding='utf-8') as f:
    f.write(he32_archive_data)

# Scrape Final Detail
final_details = {
    "Final Detail": "All data has been scraped successfully."
}
with open("final_details.txt", "w", encoding='utf-8') as f:
    for key, value in final_details.items():
        f.write(f"{key}: {value}\n")

# Clean Up
driver.quit()