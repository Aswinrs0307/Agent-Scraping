import autogen
import os
import logging
from typing import Dict, Any

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('new_scraping.log'), logging.StreamHandler()]
)

def setup_work_directory(dir_name: str) -> None:
    """Ensure work directory exists and is clean."""
    try:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            logging.info(f"Work directory '{dir_name}' created.")
        else:
            logging.info(f"Work directory '{dir_name}' already exists.")
    except Exception as e:
        logging.error(f"Error setting up work directory: {str(e)}")
        raise

def get_llm_config() -> Dict[str, Any]:
    """Get LLM configuration with error handling."""
    try:
        return {
            "cache_seed": 52,
            "config_list": autogen.config_list_from_json(
                "OAI_CONFIG_LIST.json",
                filter_dict={"model": ["Your model"]}
            ),
            "temperature": 0,
            "max_tokens": 4000  # Increased token limit for comprehensive responses
        }
    except Exception as e:
        logging.error(f"Error loading LLM config: {str(e)}")
        raise

def create_agents(llm_config: Dict[str, Any], work_dir: str):
    """Create assistant and user proxy agents with enhanced configuration."""
    try:
        assistant = autogen.AssistantAgent(
            name="web_scraping_agent",
            llm_config=llm_config,
            system_message=(
                "You are an advanced web scraping specialist. Your tasks include: "
                "analyzing website structures, simulating user actions, "
                "handling dynamic elements, and extracting data reliably."
            )
        )

        user_proxy = autogen.UserProxyAgent(
            name="user_proxy",
            human_input_mode="TERMINATE",
            max_consecutive_auto_reply=10,
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
            code_execution_config={
                "work_dir": work_dir,
                "use_docker": False
            },
            llm_config=llm_config,
            system_message="I need to scrape details from the website."
        )
        logging.info("Agents created successfully.")
        return assistant, user_proxy
    except Exception as e:
        logging.error(f"Error creating agents: {str(e)}")
        raise

def initiate_scraping(task: str, assistant, user_proxy, max_retries: int = 3):
    """Initiate scraping task with retry mechanism."""
    for attempt in range(max_retries):
        try:
            logging.info(f"Initiating scraping task, attempt {attempt + 1} of {max_retries}.")
            user_proxy.initiate_chat(assistant, message=task)
            logging.info("Scraping task completed successfully.")
            break
        except Exception as e:
            logging.error(f"Error in scraping task attempt {attempt + 1}: {str(e)}")
            if attempt == max_retries - 1:
                logging.critical("All retries failed. Exiting.")
                raise
            else:
                logging.info("Retrying...")

def main():
    """Main function to orchestrate scraping workflow."""
    work_dir = "bankofcyprus"
    setup_work_directory(work_dir)

    try:
        llm_config = get_llm_config()
        assistant, user_proxy = create_agents(llm_config, work_dir)

        url = "https://efiling.drcor.mcit.gov.cy/DrcorPublic/SearchForm.aspx?sc=0&cultureInfo=en-AU"
        name = "BANK OF CYPRUS PUBLIC COMPANY LIMITED"

        task = f"""
        You are an advanced web surfing and scraping agent. Follow the systematic instructions provided to scrape data from the website:
        Website URL: {url}
        Search Query: {name}
        Ensure all output files are saved in the '{work_dir}' directory.
        The detailed steps are outlined in the task description provided.
        Navigate to the Web site:
        Initialize the selenium web driver and load the provided {url}
    
    Perform search:
        Locate the search input field using the ID: ctl00_cphMyMasterCentral_ucSearch_txtName.
        Input the search query:{name}.
        Locate and trigger the search button using ID: ctl00_cphMyMasterCentral_ucSearch_lbtnSearch.
    
    wait for result to load:
        pause to ensure the results are fully loaded .Adjust waiting time if necessary .
    
    Navigate to Results:
        Locate the results table using the Xpath: /html/body/form/div[3]/div[3]/table/tbody/tr/td/table/tbody/tr[9]/td/div/table.
        Identify rows in the table with class="basket".
        Iterate through rows to find the correct entry:
            - Check if the onclick attribute contains "Select".
            - If the attribute matches a pattern like "__doPostBack('ctl00$cphMyMasterCentral$GridView1','Select$n')" where $n is the row index:
                * Parse $n to determine the row number.
                * If the search input {name} is in the row, store the row number.
            - If the desired row is found, trigger the onclick attribute using JavaScript to navigate to the organization details page:
                * Use a JavaScript executor to invoke: `__doPostBack('ctl00$cphMyMasterCentral$GridView1','Select$n')`.
        Log an error if no matching row is found or if there are issues with triggering the link.
    
    Scrape Organization details:
        Locate the organizaton Details Tab using the id="organizationDetailsTab".
        Extract the following fields from the ID and save them in a file named organization_details.txt:
            Name: id= ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblName
            Registration Number: id= ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblNumber
            Type : id= ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblType
            subType: id=ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblSubType
            Name Status: id=id=ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblNameStatus
            Registration Date : id=ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblRegistrationDate
            Organization Status: id=ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblStatus
            Country of Incorporation:	id="ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_trOrigingCountry"
            Status Date : id=ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblstatusDate
            Last Annual Return date : id = ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblLastAnnualReturnDate
    
    Scrape File Status:
        Locate the File Status Section using the ID: ctl00_cphMyMasterCentral_lblFileStatus.
        Extract the following fields and save them in a file named file_status.txt
        Last File Update: id=ctl00_cphMyMasterCentral_lblFileLastUpdateVal
        Pending Services: id=ctl00_cphMyMasterCentral_lblFoundNo.
    
    Scrape Additional Tables from File Status:
        Extract Table data from the Xpath:
        /html/body/form/div[3]/div[3]/div[5]/div/div/div[4]/div[2]/div[1]/div[4]/div[2]/div/table.
        id="ctl00_cphMyMasterCentral_grdPendingServices"
        Slide down to  check if there is Pagination:
        Handle pagination using the Next Page button (ID: ctl00_cphMyMasterCentral_NextPage) until disabled:
            - Locate and click the Next Page button using the element:
                **<input type="image" name="ctl00$cphMyMasterCentral$NextPage" id="ctl00_cphMyMasterCentral_NextPage" class="nextPageLink" src="Images/next20px.png" alt="Next Page" style="border-width:0px;">**
            - Continue clicking until the element:
                **<input type="image" name="ctl00$cphMyMasterCentral$NextPage" id="ctl00_cphMyMasterCentral_NextPage" disabled="disabled" class="nextPageLink" src="Images/next20px.png" alt="Next Page" style="border-width:0px;">** 
                OR until the text "n of n" (from ID `ctl00_cphMyMasterCentral_pagingInfo`) is detected.
            - Add a timeout (e.g., 10 seconds) to check if the page transition occurs. If no transition happens and the Next Page button is still clickable, log the issue and take a screenshot, then skip to the next task.
        - Once all pages are scraped:
        - Save the collected data into the file `additional_table.txt`.
        - Log completion of pagination for this section.
        - Transition to the next scraping task (e.g., "Directors and Secretaries" tab).    
    Scrape Directors and Secerataries:
        Locate and click the directors Link using the ID: ctl00_cphMyMasterCentral_directors.
        Extract table data from the Xpath:
        /html/body/form/div[3]/div[3]/div[5]/div/div/div[4]/div[2]/div[2]/div/div/table.
        ID: ctl00_cphMyMasterCentral_OfficialsGrid
        Save the table data in a file named directors_secretaries.txt.
    
    Scrape Registerd office :
        Locate and click the Registered Office Link using the ID : registeredOffice.
        Extract the address details from the "ID" address and save them in a file named registered_office.txt.
        ID:ctl00_cphMyMasterCentral_addressTitle
        Street Name: id=ctl00_cphMyMasterCentral_Street.
        Parish: id=ctl00_cphMyMasterCentral_Parish
        Teritory: id=ctl00_cphMyMasterCentral_Teritory
    
    Scrape HE32 Archive:
        Locate and click the HE32 Archive Link using the ID: HE32Archive.
        Extract the table data from the Xpath:
        /html/body/form/div[3]/div[3]/div[5]/div/div/div[4]/div[2]/div[4]/div/div/table.
        id="HE32ArchiveLi"
        id="ctl00_cphMyMasterCentral_gridHE32Archive" 
        Save the table data in a file named he32_archive.txt.
    
    Scrape Preview Files Documents:
        Locate and click the Preview File document tab using the id="ctl00_cphMyMasterCentral_lbtnPreviewFileDocuments",
        href="javascript:__doPostBack('ctl00$cphMyMasterCentral$lbtnPreviewFileDocuments','')
        Locate and find the id="ctl00_cphMyMasterCentral_rdFileType":
            Click id="ctl00_cphMyMasterCentral_rdFileType_0"
        Locate the Files Table using this Xpath:
        /html/body/form/div[3]/div[3]/div[5]/div/div[2]/div/div/table.
        id="ctl00_cphMyMasterCentral_grdFileContent"
        Locate if there is pagination using the id="ctl00_cphMyMasterCentral_NextPage",class="nextPageLink" Untill the id="ctl00_cphMyMasterCentral_pagingInfo" become "n" of "n".Here "n" is the page numbers like 1,2,3 etc... untill disabled="disabled"
            Scrape each tables.
        scrape the details and save it in a File_Documents_main.txt.
    
    Scrape Charges and montages:
        Locate and find the ID: ctl00_cphMyMasterCentral_rdFileType.
        Try clicking ID: ctl00_cphMyMasterCentral_rdFileType_1 with onclick="javascript:setTimeout('__doPostBack(\'ctl00$cphMyMasterCentral$rdFileType$1\',\'\')', 0)".
        If the tab exists:
            Locate the Files Table using this XPath: /html/body/form/div[3]/div[3]/div[5]/div/div[2]/div/div/table.
            Check for pagination using ID: ctl00_cphMyMasterCentral_NextPage until ID: ctl00_cphMyMasterCentral_pagingInfo becomes "n of n".
            If records are found, scrape the data and save it in `File_Documents_Chargesndmontages.txt`.
            If no records are found, log the message "No records found for Charges and Montages" and leave the field as an empty list in the JSON output.
        scrape the details and save it in a File_Documents_Chargesndmontages.txt.
    
    Scrape Translations:
        Try clicking ID: ctl00_cphMyMasterCentral_rdFileType_2 with onclick="javascript:setTimeout('__doPostBack(\'ctl00$cphMyMasterCentral$rdFileType$2\',\'\')', 0)".
        If the tab exists:
            Locate the Files Table using this XPath: /html/body/form/div[3]/div[3]/div[5]/div/div[2]/div/div/table.
            Check for pagination using ID: ctl00_cphMyMasterCentral_NextPage until ID: ctl00_cphMyMasterCentral_pagingInfo becomes "n of n".
            If records are found, scrape the data and save it in `File_Documents_Translation.txt`.
            If no records are found, log the message "No records found for Translations" and leave the field as an empty list in the JSON output.
        scrape the details and save it in a File_Documents_Translation.txt.
        
    
    Scrape final details from the save .txt file:
        The output should be in the JSON UTF-o8 and ensure_ascii=False format like:
            ```json
                "Organization details":[...],
                "File Status":[..],
                "Additional Tables":[...],
                "Directors and Secretaries":[...],
                "HE32 Archive":[...],
                "Registered Office":[...],
                "Preview File Type":[...]
            ```
        Save Generated code:
            Save generated code from the response in .py file and save it.
        Clean Up
        Close the browser after all scraping tasks are complete.         
        """
        initiate_scraping(task, assistant, user_proxy)

    except Exception as e:
        logging.critical(f"Fatal error encountered: {str(e)}")
        raise

if __name__ == "__main__":
    main()
