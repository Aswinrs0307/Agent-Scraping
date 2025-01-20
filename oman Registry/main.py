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
            "cache_seed": 62,
            "config_list": autogen.config_list_from_json(
                "OAI_CONFIG_LIST.json",
                filter_dict={"model": [""]}
            ),
            "temperature": 0,
            "max_tokens": 5000  # Increased token limit for comprehensive responses
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
    work_dir = "Housing_bank"
    setup_work_directory(work_dir)

    try:
        llm_config = get_llm_config()
        assistant, user_proxy = create_agents(llm_config, work_dir)

        url = "https://www.business.gov.om/portal/searchEstablishments"
        name = "بنك الاسكان العماني"

        task = f"""
        You are an advanced web surfing and scraping agent.You must generate a code and execute the code and save it for future process. Follow the systematic instructions provided to scrape data from the website:
        Website URL: {url}
        Search Query: {name}
        Ensure all output files are saved in the '{work_dir}' directory.
        The detailed steps are outlined in the task description provided.
        Navigate to the Web site:
            Initialize the Selenium web driver and load the provided {url}. Ensure the browser and driver versions are compatible to prevent runtime errors.
        Language selection:
            Locate and click the Language selection from the provided selector "#header > div > div > div.submenu-line.pull-right > div > a". Validate that the action successfully updates the page language.
        Perform search:
            Locate the search input field using the id="search_company_name".
            Input the search query: {name}.
        Handle Captcha:
            Wait for 10 second for human interaction directly with that web site .
        Submit Search:
            Trigger the search button using the selector #searchCompanyForm > div > div.row > div:nth-child(5) > button.
        Wait for result to load:
            Pause to ensure the results are fully loaded. Use explicit waits instead of fixed delays to improve reliability.
        Navigate to Results:
            Locate the results table using the XPath: /html/body/div[2]/div[2]/div/div/div/table.
        Check if pagination exists after no exact match:
            Inspect for pagination using the XPath: /html/body/div[2]/div[2]/div/div/div/ul.
            Initially, compare the company name in the table rows with {name}. If an exact match is found, locate the "View" button embedded in the <a> tag containing the href and click it to navigate to the details page.
            If there are multiple similar matches, continue checking all pages through pagination to find the exact match. Only proceed to pagination if no exact match is found on the current page.
            If pagination is necessary and the href value of the pagination link is not "#", continue clicking the "Next Page" button using the <a> tag href.
            Repeat this process until either:
                1. An exact match for the search query {name} is found in the table rows.
                2. The href of the pagination link changes to "#", indicating the last page.
            If only one result exists and matches {name}, click the "View" button to navigate to the details page immediately, without further pagination.
        Scrape Details from Tabs:
        Handle each tab dynamically based on its visibility, determined by the class attribute:
            If the tab's class is "accordion-toggle pull-left", do not click the tab. The panel is already expanded, so directly scrape the details.
            If the tab's class is "accordion-toggle pull-left collapsed", click the tab to expand it and reveal the details.
            The default state of the tabs corresponds to class="accordion-toggle pull-left", and the visible panel has class="panel-collapse collapse in".
        Dynamically handle each tab based on its presence. Adjust the nth-child value dynamically based on the presence or absence of tabs, as follows:
                - If a tab is absent, the nth-child value decreases accordingly.
                - If a new tab is added, the nth-child value increases accordingly.
            Based on the commercial tab the dynamic value will change .
            1.Scrape Commercial Name tab:
            check and locate tab using the Xpath: /html/body/div[2]/div[2]/div[2]/div[2]/div[1]/h2/a.
            If present, scrape the below details from this selectors:#commercialNameSection > div > div:
            - Arabic Name: /html/body/div[2]/div[2]/div[2]/div[2]/div[2]/div/div/div[1]/div/text().
            - English Name: /html/body/div[2]/div[2]/div[2]/div[2]/div[2]/div/div/div[2]/div/text().
            Save to "commercial_name_details.txt".

            2.scrape Legal Type tab:
            scroll down and Check for the tab using the Xpath: /html/body/div[2]/div[2]/div[2]/div[dynamic value]/div[1]/h2/a
            If present, scrape the below details from the selectors: #legalTypeSection > div > div:
            - Legal Type: /html/body/div[2]/div[2]/div[2]/div[3]/div[2]/div/div/div/div/text().
            Save to "legal_type.txt".

            3.Scrape Registry Information tab:
            scroll down and Check for the tab using the Xpath: /html/body/div[2]/div[2]/div[2]/div[dynamic value]/div[1]/h2/a
            If present, scrape the below details from the selectors:#registryInformationSection > div > div:
            - Commercial Registration No: /html/body/div[2]/div[2]/div[2]/div[4]/div[2]/div/div/div[1]/div/p.
            - Registration Date: /html/body/div[2]/div[2]/div[2]/div[4]/div[2]/div/div/div[2]/div/p.
            - Registration Status:/html/body/div[2]/div[2]/div[2]/div[4]/div[2]/div/div/div[3]/div/p.
            - Expiry Date: /html/body/div[2]/div[2]/div[2]/div[4]/div[2]/div/div/div[4]/div/p.
            Save to "registry_information.txt".

            4.Scrape Address tab:
            Take time to scrape these details.
            scroll down and Check for the tab using the Xpath: /html/body/div[2]/div[2]/div[2]/div[dynamic value]/div[1]/h2/a
            If present, scrape the below details from this selector: #companyAddressSection > div > div:
            - Business Location: /html/body/div[2]/div[2]/div[2]/div[5]/div[2]/div/div/div[1]/div/div/text().
            - Street Name English:/html/body/div[2]/div[2]/div[2]/div[5]/div[2]/div/div/div[2]/div/div[1]/div/text().
            - Street Name Arabic: /html/body/div[2]/div[2]/div[2]/div[5]/div[2]/div/div/div[3]/div/div[1]/div/text().
            - Way Number: /html/body/div[2]/div[2]/div[2]/div[5]/div[2]/div/div/div[2]/div/div[2]/div/text().
            - Postal Code:/html/body/div[2]/div[2]/div[2]/div[5]/div[2]/div/div/div[3]/div/div[2]/div/text().
            - Building Number: /html/body/div[2]/div[2]/div[2]/div[5]/div[2]/div/div/div[2]/div/div[3]/div/text().
            - P.O. Box: /html/body/div[2]/div[2]/div[2]/div[5]/div[2]/div/div/div[3]/div/div[3]/div/text().
            - Block Number:/html/body/div[2]/div[2]/div[2]/div[5]/div[2]/div/div/div[2]/div/div[4]/div/text().
            - Latitude: //*[@id="companyAddressSection"]/div/div/div[3]/div/div[4]/div/p/text().
            - Unit Number: /html/body/div[2]/div[2]/div[2]/div[5]/div[2]/div/div/div[2]/div/div[5]/div/text().
            - Longitude://*[@id="companyAddressSection"]/div/div/div[3]/div/div[5]/div/p/text().
            Save to "address.txt".

            5.Scrape Contact Information tab:
            Take time to scrape these details
            scroll down and Check for the tab using the Xpath: /html/body/div[2]/div[2]/div[2]/div[dynamic value]/div[1]/h2/a
            If present, scrape the below details from this selector:#contactInformationSection > div > div > div:nth-child(1):
            - E-mail:/html/body/div[2]/div[2]/div[2]/div[6]/div[2]/div/div/div[1]/div[1]/div/text().
            - Mobile Number:/html/body/div[2]/div[2]/div[2]/div[6]/div[2]/div/div/div[1]/div[2]/div/text().
            Save to "contact_information.txt".

            6.Scrape Capital tab:
            Take time to scrape this details.
            scroll down and Check for the tab using the Xpath: /html/body/div[2]/div[2]/div[2]/div[dynamic value]/div[1]/h2/a
            If present, scrape the below details from this selector:#capitalSection > div > div:
            - Cash Capital: /html/body/div[2]/div[2]/div[2]/div[7]/div[2]/div/div/div[1]/div/div[1]/div/text().
            - Asset Capital: /html/body/div[2]/div[2]/div[2]/div[7]/div[2]/div/div/div[1]/div/div[2]/div/text().
            - Total Capital: /html/body/div[2]/div[2]/div[2]/div[7]/div[2]/div/div/div[1]/div/div[3]/div/text().
            - Share Count: /html/body/div[2]/div[2]/div[2]/div[7]/div[2]/div/div/div[2]/div/div[1]/div/text().
            - Share Value: /html/body/div[2]/div[2]/div[2]/div[7]/div[2]/div/div/div[2]/div/div[2]/div/text().
            Save to "capital.txt".

            7.Scrape Fiscal Information tab:
            Take time to scrape this details.
            scroll down and Check for the tab using the Xpath: /html/body/div[2]/div[2]/div[2]/div[dynamic value]/div[1]/h2/a.
            If present, scrape the below details from this selector:#fiscalInformationSection > div > div:
                CR Establishment Date:/html/body/div[2]/div[2]/div[2]/div[8]/div[2]/div/div/div[1]/div/div/div/text().
                First Financial Year End: /html/body/div[2]/div[2]/div[2]/div[8]/div[2]/div/div/div[2]/div/div[1]/div/text().
                Fiscal Year End:/html/body/div[2]/div[2]/div[2]/div[8]/div[2]/div/div/div[2]/div/div[2]/div/text().
            Save to "fiscal_information.txt".

            8.Scrape Business Activities tab:
            Take time to scrape the details.
            scroll down and Check for the tab using the Xpath: /html/body/div[2]/div[2]/div[2]/div[dynamic value]/div[1]/h2/a
            If present, scrape the below details from this selector:#declaredActivitiesSection > div > div > table:
            For Table headers scrape the details from this selectors:#declaredActivitiesSection > div > div > table > thead.
            For Table records scrape the data from this selectors:#declaredActivitiesSection > div > div > table > tbody.
            Save to "business_activities.txt".

            9.Scrape Investors tab:
            Take time to scrape the details.
            scroll down and Check for the tab using the Xpath: /html/body/div[2]/div[2]/div[2]/div[dynamic value]/div[1]/h2/a
            locate this selector:#investorsSection > div > div > table.
            For table header locate this selectors:#investorsSection > div > div > table > thead.            
            For detailed investor information:
            1. Find all rows with class="accordion-toggle tr-collapse collapsed" and click.
            2. For each row (indexed from 0 to n):
                - Store the row index number (starting from 0)
                - Click the row using selector: #investorsSection > div > div > table > tbody > tr.accordion-toggle.tr-collapse.collapsed
                - Wait for the detailed section to load using data-target="#row_id__investors_(index)"
                - Extract all information from the expanded section including:
                    * Name (Arabic/English)
                    * Nationality
                    * ID Type and Number
                    * Number of Shares
                    * Share Percentage
                    * Additional Details (if any)
                - Store the complete details for each investor in a structured format investor_details.txt
            3. Save all investor details to "investor_details.txt"
            
            10.Scrape Authorized Signatories tab:
            Take time to scrape the details.
            scroll down and Check for the tab using the Xpath: /html/body/div[2]/div[2]/div[2]/div[dynamic value]/div[1]/h2/a
            locate this selector:#signatoriesSection > div > div > table.
            For table header locate this selector:#signatoriesSection > div > div > table > thead            
            For detailed signatory information:
            1. Find all rows with class="accordion-toggle tr-collapse collapsed" click.
            2. For each row (indexed from 0 to n):
                - Store the row index number (starting from 0)
                - Click the row using selector: #signatoriesSection > div > div > table > tbody > tr.accordion-toggle.tr-collapse.collapsed
                - Wait for the detailed section to load using data-target="#row_id__signatories_(index)"
                - Extract all information from the expanded section including:
                    * Name (Arabic/English)
                    * Nationality
                    * ID Type and Number
                    * Position/Title
                    * Signing Authorities
                    * Additional Details (if any)
                - Store the complete details for each signatory in a structured format Authorized_details.txt
            3. Save all signatory details to "signatory_details.txt"
            
            11.Scrape Auditor tab:
            Take time to scrape the details.
            scroll down and Check for the tab using the Xpath: /html/body/div[2]/div[2]/div[2]/div[dynamic value]/div[1]/h2/a
            locate this selector:#auditorsSection > div > div > table.
            For table header locate this selectors:#auditorsSection > div > div > table > thead.            
            For detailed auditor information:
            1. Find all rows with class="accordion-toggle tr-collapse collapsed" and click.
            2. For each row (indexed from 0 to n):
                - Store the row index number (starting from 0)
                - Click the row using selector: #auditorsSection > div > div > table > tbody > tr.accordion-toggle.tr-collapse.collapsed
                - Wait for the detailed section to load using data-target="#row_id__auditors_(index)"
                - Extract all information from the expanded section including:
                    * Name (Arabic/English)
                    * License Number
                    * Registration Number
                    * Contact Information
                    * Additional Details (if any)
                - Store the complete details for each auditor in a structured format as auditor_details.txt
            3. Save all auditor details to "auditor_details.txt"
            
            12.Scrape Licenses tab:
            Take time to scrape the details.
            sccroll down and Check for the tab using the selector: #content > div:nth-child(dynamic_value) > div.panel-heading > h2 > a.
            Locate the selectors: #licenseSection > div > table.
            For table header scrape this selectors: #licenseSection > div > table > thead.
            If present, scrape the table: /html/body/div[2]/div[2]/div[2]/div[12]/div[2]/div/table/tbody.
            Save to "licenses.txt".

        Scrape final details from the saved .txt files:
        The output should be in the JSON UTF-8 and ensure_ascii=False format, structured like:
        ```json
            "Commercial Name": [...],
            "Legal Type": [...],
            "Registry Information": [...],
            "Address": [...],
            "Contact Information": [...],
            "Capital": [...],
            "Fiscal Information": [...],
            "Business Activities": [...],
            "Investors": [...],
            "Authorized Signatories": [...],
            "Auditor": [...],
            "Licenses": [...]
        ```

        Save Generated Code:
        Save the generated code from the response in a .py file and save it.
        Clean Up:
        Close the browser after all scraping tasks are complete.
"""
        initiate_scraping(task, assistant, user_proxy)
    except Exception as e:
        logging.critical(f"Fatal error encountered: {str(e)}")
        raise

if __name__ == "__main__":
    main()
