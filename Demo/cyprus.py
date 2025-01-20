import streamlit as st
import os
import time
from datetime import datetime, timedelta
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import random
import pandas as pd


def format_time(seconds):
    return str(timedelta(seconds=int(seconds)))
def update_progress(progress_bar, time_placeholder, start_time, progress, status):
    progress_bar.progress(progress)
    time_placeholder.text(f"⏱️ Elapsed Time: {format_time(time.time() - start_time)} | {status}")
def Scraping(url,name,headless,progress_bar, time_placeholder):
    start_time = time.time()
    # Create directory for output files
    Company_name = "".join(c if c.isalnum() or c.isspace() else "_" for c in name).strip()
    output_dir = Company_name
    os.makedirs(output_dir, exist_ok=True)
    # Initialize progress
    update_progress(progress_bar, time_placeholder, start_time, 0, "Starting...")
    time.sleep(1)  # Simulate initial setup
    # Initialize the Selenium WebDriver
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")  # Disable GPU (useful for certain environments)
    chrome_options.add_argument("--no-sandbox")  # Avoid sandboxing issues (useful for Docker)
    chrome_options.add_argument("--disable-dev-shm-usage")  # Prevent shared memory issues
    chrome_options.add_argument("--window-size=1920,1080")  # Set screen size (useful for screenshots)
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    update_progress(progress_bar, time_placeholder, start_time, 10, "Setting up browser...")
    time.sleep(1)  # Simulate browser setup

    # Spoof the User-Agent to make the request look like it's from a regular browser
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
    ]

    # Randomly choose a user-agent from the list
    user_agent = random.choice(user_agents)
    chrome_options.add_argument(f"user-agent={user_agent}")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)  # or use webdriver.Firefox() or any other browser
    driver.get(url)

    update_progress(progress_bar, time_placeholder, start_time, 20,"Working on ....")
    time.sleep(1)  # Simulate browser setup
    # Perform search
    search_input = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucSearch_txtName")
    search_input.send_keys(name)
    search_button = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucSearch_lbtnSearch")
    search_button.click()

    # Wait for results to load
    wait = WebDriverWait(driver, 10)  # Wait for up to 10 seconds

    # Find the correct entry on the current page
    row_number = None
    while True:
        try:
            # Navigate to Results
            results_table = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/form/div[3]/div[3]/table/tbody/tr/td/table/tbody/tr[9]/td/div/table")))
            rows = results_table.find_elements(By.CLASS_NAME, "basket")
            # Loop through the rows on the current page
            for index, row in enumerate(rows):
                if "Select" in row.get_attribute("onclick"):
                    if name in row.text:  # Check if the name matches
                        row_number = index  # Store the row number
                        break  # Exit the loop if the name is found

            if row_number is not None:
                # If row_number is found, break the loop and move to organization details page
                break

            # If row_number is still None, check pagination and go to the next page
            next_page_button = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_NextPage")
            if "disabled" in next_page_button.get_attribute("outerHTML"):
                # If no next page is available, exit the loop
                print("No matching result found for the search query")
                break
            else:
                # Otherwise, click the next page and wait for it to load
                next_page_button.click()
                time.sleep(5)  # Wait for the next page to load

        except Exception as e:
            print(f"Error: {e}")
            break

    if row_number is not None:
        # Once row_number is found, trigger the onclick action to view the organization details
        driver.execute_script(f"__doPostBack('ctl00$cphMyMasterCentral$GridView1','Select${row_number}')")
    else:
        print("No matching row found.")
        driver.quit()
        exit()

    # Scrape Organization details
    time.sleep(5)  # Wait for the details to load
    organization_details = {}
    # organization_details['Name'] = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblName").text
    # organization_details['Registration Number'] = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblNumber").text  
    # organization_details['Type'] = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblType").text
    # organization_details['SubType'] = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblSubType").text
    # organization_details['Name Status'] = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblNameStatus").text      
    # organization_details['Registration Date'] = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblRegistrationDate").text
    # organization_details['Organization Status'] = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblStatus").text  
    # organization_details['Country of Incorporation'] = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_trOrigingCountry").text
    # organization_details['Status Date'] = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblstatusDate").text      
    # organization_details['Last Annual Return Date'] = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblLastAnnualReturnDate").text

    # Dictionary of field IDs and their corresponding keys
    field_mappings = {
        'Name': "ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblName",
        'Registration Number': "ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblNumber",
        'Type': "ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblType",
        'SubType': "ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblSubType",
        'Name Status': "ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblNameStatus",
        'Registration Date': "ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblRegistrationDate",
        'Organization Status': "ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblStatus",
        'Country of Incorporation': "ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_trOrigingCountry",
        'Status Date': "ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblstatusDate",
        'Last Annual Return Date': "ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblLastAnnualReturnDate"
    }

    # Iterate through fields and handle missing ones gracefully
    for field_name, field_id in field_mappings.items():
        try:
            element = driver.find_element(By.ID, field_id)
            organization_details[field_name] = element.text
        except Exception as e:
            print(f"Field '{field_name}' not found: {str(e)}")
            organization_details[field_name] = "Not Available"

    # Save organization details
    with open(os.path.join(output_dir, 'organization_details.txt'), 'w', encoding='utf-8') as f:
        for key, value in organization_details.items():
            f.write(f"{key}: {value}\n")

    update_progress(progress_bar, time_placeholder, start_time, 30,"Working on ...")
    time.sleep(1)  # Simulate browser setup
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
            # Extract headers
            headers = []
            header_cells = additional_table.find_elements(By.TAG_NAME, "th")
            if header_cells:
                for header in header_cells:
                    headers.append(header.text)
            else:
                headers=None

            if not headers:
                additional_table_data.append(["No data available"])

            #Append headers to the table data
            additional_table_data.append(headers)
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

    update_progress(progress_bar, time_placeholder, start_time, 35,"Working on ...")
    time.sleep(1)  # Simulate browser setup
    # Scrape Directors and Secretaries
    driver.find_element(By.ID, "ctl00_cphMyMasterCentral_directors").click()
    time.sleep(5)  # Wait for the details to load
    directors_data = []
    directors_table = driver.find_element(By.XPATH, "/html/body/form/div[3]/div[3]/div[5]/div/div/div[4]/div[2]/div[2]/div/div/table")
    headers = []
    header_cells = directors_table.find_elements(By.TAG_NAME, "th")
    if header_cells:
        for header in header_cells:
            headers.append(header.text)
    else:
        headers=None
    if not headers:
        directors_data.append(["No data available"])
    directors_data.append(headers)
    rows = directors_table.find_elements(By.TAG_NAME, "tr")
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        directors_data.append([cell.text for cell in cells])

    update_progress(progress_bar, time_placeholder, start_time, 40,"Working on ...")
    time.sleep(1)  # Simulate browser setup
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

    update_progress(progress_bar, time_placeholder, start_time, 45,"Working on ...")
    time.sleep(1)  # Simulate browser setup
    # Scrape HE32 Archive
    driver.find_element(By.ID, "HE32Archive").click()
    time.sleep(5)  # Wait for the details to load
    he32_archive_data = []

    # Try to find the table
    try:
        he32_table = driver.find_element(By.XPATH, "/html/body/form/div[3]/div[3]/div[5]/div/div/div[4]/div[2]/div[4]/div/div/table")
        # Extract headers
        headers = []
        header_cells = he32_table.find_elements(By.TAG_NAME, "th")
        
        if not header_cells:
            st.write("")
        else:
            for header in header_cells:
                headers.append(header.text)
            he32_archive_data.append(headers)
        
        # Extract rows
        rows = he32_table.find_elements(By.TAG_NAME, "tr")
        if not rows:
            st.write("")
        else:
            for row in rows:
                # Check if there is a "No records found" message in a td tag
                if "No records found" in row.text:
                    st.write("No data available for HE32 Archive (No records found).")
                    break
                cells = row.find_elements(By.TAG_NAME, "td")
                he32_archive_data.append([cell.text for cell in cells])

    except Exception as e:
        print(f"Error scraping HE32 Archive: {e}")
        st.write("No data available for HE32 Archive (error occurred).")

    # If there is no data found or no headers, make sure it's reflected in the output
    if not he32_archive_data:
        he32_archive_data = "No data available"

    # Save HE32 archive data
    with open(os.path.join(output_dir, 'he32_archive.txt'), 'w', encoding='utf-8') as f:
        if isinstance(he32_archive_data, list):
            for row in he32_archive_data:
                f.write("\t".join(row) + "\n")
        else:
            f.write(he32_archive_data)


    update_progress(progress_bar, time_placeholder, start_time, 50,"Working on ...")
    time.sleep(1)  # Simulate browser setup
    # Initialize preview files, charges, and translations data
    preview_files = []
    charges_mortgages = []
    translations = []

    # Function to scrape data for a specific type
    def scrape_file_type(file_type_id, result_list):
        try:
            driver.find_element(By.ID, file_type_id).click()
            time.sleep(2)  # Wait for the page to load
            
            while True:
                table = driver.find_element(By.XPATH, "/html/body/form/div[3]/div[3]/div[5]/div/div[2]/div/div/table")
                headers = []
                header_cells = table.find_elements(By.TAG_NAME, "th")
                if header_cells:
                    for header in header_cells:
                        headers.append(header.text)
                else:
                    headers=None
                if not headers:
                    result_list.append(["No data available"])
                result_list.append(headers)
                rows = table.find_elements(By.TAG_NAME, "tr")
                for row in rows:
                    result_list.append([cell.text for cell in row.find_elements(By.TAG_NAME, "td")])

                try:
                    next_button = driver.find_element(By.ID, "ctl00_cphMyMasterCentral_NextPage")
                    if "disabled" in next_button.get_attribute("outerHTML"):
                        break
                    next_button.click()
                    time.sleep(2)  # Wait for the next page to load
                except Exception as e:
                    print(f"Error navigating to next page for {file_type_id}: {e}")
                    break
        except Exception as e:
            print(f"Error scraping data for {file_type_id}: {e}")

    update_progress(progress_bar, time_placeholder, start_time, 55,"Working on ...")
    time.sleep(1)  # Simulate browser setup
    # Main scraping logic
    preview_provided = False
    charges_provided = False
    translations_provided = False

    # Scrape Preview Files
    try:
        driver.find_element(By.ID, "ctl00_cphMyMasterCentral_lbtnPreviewFileDocuments").click()
        time.sleep(2)  # Wait for the page to load
        scrape_file_type("ctl00_cphMyMasterCentral_rdFileType_0", preview_files)
        preview_provided = True
    except Exception:
        print("Preview Files type not provided.")

    # Scrape Charges and Mortgages
    try:
        scrape_file_type("ctl00_cphMyMasterCentral_rdFileType_1", charges_mortgages)
        charges_provided = True
    except Exception:
        print("Charges and Mortgages type not provided.")

    # Scrape Translations
    try:
        scrape_file_type("ctl00_cphMyMasterCentral_rdFileType_2", translations)
        translations_provided = True
    except Exception:
        print("Translations type not provided.")

    update_progress(progress_bar, time_placeholder, start_time, 60,"Working on ...")
    time.sleep(1)  # Simulate browser setup
    # Compile the results into JSON-friendly format
    output_data = {
        "Preview File Type": preview_files if preview_provided else "Not Provided",
        "Charges and Mortgages": charges_mortgages if charges_provided else "Not Provided",
        "Translations": translations if translations_provided else "Not Provided"
    }

    # Handle empty records within provided types
    if preview_provided and not preview_files:
        output_data["Preview File Type"] = []

    if charges_provided and not charges_mortgages:
        output_data["Charges and Mortgages"] = []

    if translations_provided and not translations:
        output_data["Translations"] = []

    # Compile all data into JSON format
    output_data = {
        "Organization details": organization_details,
        "File Status": file_status,
        "Additional Tables": additional_table_data,
        "Directors and Secretaries": directors_data,
        "HE32 Archive": he32_archive_data,
        "Registered Office": registered_office,
        "Preview File Type": preview_files if preview_files else [],
        "Charges and Mortgages": charges_mortgages if charges_mortgages else [],
        "Translations": translations if translations else []
    }

    # Save JSON output
    with open(os.path.join(output_dir, 'output.json'), 'w', encoding='utf-8') as json_file:
        json.dump(output_data, json_file, ensure_ascii=False, indent=4)

    # Clean Up
    driver.quit()

    update_progress(progress_bar, time_placeholder, start_time, 65, "Fetching details...")
    time.sleep(1)  # Simulate data fetching

    update_progress(progress_bar, time_placeholder, start_time, 70, "Processing information...")
    time.sleep(1)  # Simulate processing

    update_progress(progress_bar, time_placeholder, start_time, 80, "Gathering data...")
    time.sleep(1)  # Simulate data gathering

    update_progress(progress_bar, time_placeholder, start_time, 90, "Saving results...")
    time.sleep(1)  # Simulate saving

    update_progress(progress_bar, time_placeholder, start_time, 100, "Completed!")
    return os.path.join(output_dir, 'output.json')