import autogen
llm_config={
    "cache_seed": 6,  # change the seed for different trials
    "config_list": autogen.config_list_from_json(
        "OAI_CONFIG_LIST.json",
        filter_dict={"model": ["model name"]},
    ),
    "temperature": 0.3,
    "max_tokens":1000
}

assistant=autogen.AssistantAgent(
    name="Web_Scraping_Agent",
    llm_config=llm_config
)

user_proxy=autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode='TERMINATE',
    max_consecutive_auto_reply=5,
    is_termination_msg=lambda x:x.get("content"," ").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir":"Generated","use_docker":False},
    llm_config=llm_config,
    system_message="""You are a web scraping agent and I need to scrape particular details from a web site """
)

url="https://efiling.drcor.mcit.gov.cy/DrcorPublic/SearchForm.aspx?sc=0&cultureInfo=en-AU"
Query="BANK OF CYPRUS PUBLIC COMPANY LIMITED"
task=f"""
    Task Description:
    You are a web scraping agent tasked with extracting specific information from any provided URL. Your responsibilities include analyzing the website's structure, locating elements based on IDs, names, and class names, and extracting data effectively. Follow the detailed steps below:

    Steps:
    1.Extract HTML Structure:
        1.Scrape the HTML content of the provided website URL ({url}).

    2.Search Input Fields:
        1.Identify and extract all text input fields related to searching.
        2.Use attributes such as id, name, and class to locate these fields.
        3.To get all ID , names and Classname of a text field for searching input and then try to give the user {Query}
    
    3.Find and Interact with the Search Button or Link:
        1.Identify the element responsible for triggering the search. It may be:
            1.A clickable button (<button> or input type="submit">) with attributes like onclick.
            2.A clickable link (<a> tag) acting as a search trigger.
            3.Elements with the class name button or similar, even if it's not a <button> tag.
            4.Note its attributes and behavior.
        2.Simulate entering the {Query} into the detected input field and clicking the respective button or link.
    
    4.Enter the input:
        1.After you find the correct ID or name or classname of a Text field for input , you should enter the {Query}.
        2.Here the user can give any input that will be a name or ID as a input as {Query}
        3.After entering the detail ,next try to scrape the button used in this web site,there is a onclick button ,it could be in any name.once you find the button field and then click the respected button for searching.
    
    5.Perform Search Action:
        1.Simulate entering the provided search term ({Query}) into the relevant input field.
        2.Simulate clicking the identified search triggering content.
    
    6.Handle Search Results:
        1.If the search result opens another link or page, extract the HTML content of the new page.
        2.Search for any links, text, or details related to the {Query} on the result page.
    
    7.Extract Details:
        1.Scrape the relevant information pertaining to {Query} from the search results.
        2.If a related link appears, open that link, scrape it, and extract the required details.
    
    8.Output Results:
        1.Present the retrieved details related to {Query} in plain text format.
"""

user_proxy.initiate_chat(
    assistant,
    message=task
)