import autogen
llm_config={
    "cache_seed": 4,  # change the seed for different trials
    "config_list": autogen.config_list_from_json(
        "OAI_CONFIG_LIST.json",
        filter_dict={"model": ["Model name"]},
    ),
    "temperature": 0,
    "max_tokens":2500
}

assistant=autogen.AssistantAgent(
    name="Web_Scraping_Agent",
    llm_config=llm_config
)

user_proxy=autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode='TERMINATE',
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x:x.get("content"," ").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir":"Result","use_docker":False},
    llm_config=llm_config,
    system_message="""I need to scrape details from a web site """
)

url="https://efiling.drcor.mcit.gov.cy/DrcorPublic/SearchForm.aspx?sc=0&cultureInfo=en-AU"
Query="BANK OF CYPRUS PUBLIC COMPANY LIMITED"
task=f"""
    You are a advanced web scraping agent and you tasked with automating the extraction of data from a given website. Your role involves analyzing the website’s structure, identifying key elements like input fields, triggers, and interactive elements, simulating user actions, and efficiently retrieving relevant information. The process should be adaptable to different web structures, account for dynamic content, and manage state persistence for reliable and uninterrupted execution.The extracted results must strictly align with the expected content visible on the provided URL without introducing unrelated elements such as arbitrary dates, times, or other extraneous data. Follow the steps outlined below to complete this task systematically.

    Website URL to Scrape: {url}

    Steps to Follow:
    Navigate to the Website
        Initialize the Selenium WebDriver and load the provided {url}.
    Perform Search
        Locate the search input field using the ID: ctl00_cphMyMasterCentral_ucSearch_txtName.
        Input the search query: {Query}.
        Locate and trigger the search button using ID: ctl00_cphMyMasterCentral_ucSearch_lbtnSearch.
    
    Wait for Results to Load
        Pause to ensure the results are fully loaded. Adjust waiting time if necessary.
        
    Navigate to Results
        Locate the first result using the XPath: //a[contains(text(), 'Select')].
        Trigger the "Select" link using JavaScript to navigate to the organization details page.
        
    Scrape Organization Details
        Locate the Organization Details Tab using the ID: organizationDetailsTab.
        Extract the following fields from the ID and save them in a file named organization_details.txt:
        Name : id=ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblName
        Registration Number: id=ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblNumber
        Type : id = ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblType
        Subtype : id=ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblSubType
        Name Status: id=ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblNameStatus
        Registration Date : id=ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblRegistrationDate
        Organization Status: id=ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblStatus
        Status Date : id=ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblstatusDate
        Last Annual Return Date : id = ctl00_cphMyMasterCentral_ucOrganizationDetailsSummary_lblLastAnnualReturnDate
        
    Scrape File Status
        Locate the File Status Section using the ID: ctl00_cphMyMasterCentral_lblFileStatus.
        Extract the following fields and save them in a file named file_status.txt:
        Last File Update : id=ctl00_cphMyMasterCentral_lblFileLastUpdateVal
        Pending Services : id=ctl00_cphMyMasterCentral_lblFoundNo
        
    Scrape Additional Tables
        Extract table data from the XPath:
        /html/body/form/div[3]/div[3]/div[5]/div/div/div[4]/div[2]/div[1]/div[4]/div[2]/div/table.
        id="ctl00_cphMyMasterCentral_grdPendingServices"
        Save the table data in a file named additional_table.txt.
        
    Scrape Directors and Secretaries
        Locate and click the Directors Link using the ID: ctl00_cphMyMasterCentral_directors.
        Extract table data from the XPath:
        /html/body/form/div[3]/div[3]/div[5]/div/div/div[4]/div[2]/div[2]/div/div/table.
        ID: ctl00_cphMyMasterCentral_OfficialsGrid
        Save the table data in a file named directors_secretaries.txt.
        
    Scrape Registered Office
        Locate and click the Registered Office Link using the ID: registeredOffice.
        Extract the address details from the "ID" address and save them in a file named registered_office.txt.
        ID: ctl00_cphMyMasterCentral_addressTitle
        Street Name: ID ctl00_cphMyMasterCentral_Street
        ID : ctl00_cphMyMasterCentral_Parish
        ID: ctl00_cphMyMasterCentral_Teritory        
    Scrape HE32 Archive
        Locate and click the HE32 Archive Link using the ID: HE32Archive.
        Extract table data from the XPath:
        /html/body/form/div[3]/div[3]/div[5]/div/div/div[4]/div[2]/div[4]/div/div/table.
        id="HE32ArchiveLi"
        id="ctl00_cphMyMasterCentral_gridHE32Archive"        
        Save the table data in a file named he32_archive.txt.
        
    Scrape Final Detail:
        Save this information in a file named final_details.txt.
        
    Clean Up
        Close the browser after all scraping tasks are complete.
"""

user_proxy.initiate_chat(
    assistant,
    message=task
)