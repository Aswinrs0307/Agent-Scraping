import autogen
llm_config={
    "cache_seed": 1,  # change the seed for different trials
    "config_list": autogen.config_list_from_json(
        "OAI_CONFIG_LIST.json",
        filter_dict={"model": ["model name"]},
    ),
    "temperature": 0.3,
    "max_tokens":2000
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
    code_execution_config={"work_dir":"Generated_Result","use_docker":False},
    llm_config=llm_config,
    system_message="""You are a web scraping agent and I need to scrape particular details from a web site """
)

url="https://efiling.drcor.mcit.gov.cy/DrcorPublic/SearchForm.aspx?sc=0&cultureInfo=en-AU"
Query="BANK OF CYPRUS PUBLIC COMPANY LIMITED"
task=f"""
    **Task Description**:  
    You are a web scraping agent responsible for automating the extraction and interaction with data from a given website. Your task involves analyzing the website's structure, identifying elements such as input fields and triggers, simulating user actions, and retrieving relevant information efficiently. Follow the detailed steps below to complete the task.
    
    **Steps to Follow**:
    1. Extract the HTML Structure  
        1. Fetch the HTML content of the provided URL ({url}).  
        2. Analyze the DOM to identify input fields, links, buttons, and other interactive elements.
        3.Store the HTML structure for future reference.
    
    2. Locate Search Input Fields  
        1. Identify all text input fields related to search functionality by examining:  
            - <input> tags with attributes like id, name, class, or placeholder.  
            - Fields with type="text", aria-label, or contextual hints from <label> tags or nearby elements.  
        2. Document the attributes (id, name, class, placeholder).
        3.Save input fields and attributes for re-use.    
    
    3. Identify the Search Trigger  
        1. Locate the element that initiates the search, which might include:  
            - A <button> tag, <input type="submit">, or <a> tag styled as a button.
            - Also look for an anchor (<a>) tag that executes a __doPostBack function.Document the id, href, or any associated onclick attributes for future interactions.  
            - Divs, spans, or other clickable elements with event listeners (onclick, onkeypress) or accessibility attributes (claasname="button" or "buttons" or "btn").  
        2. If no explicit trigger exists, look for alternatives like form submissions or JavaScript events (e.g., Enter key).
        4.Document the trigger’s attributes (e.g., onclick, id, class) for interaction.
    
    4. Simulate User Input  
        1. Enter the provided search term ({Query}) into the identified input field using its documented attributes.  
        2. Simulate user interaction by clicking the trigger or submitting the form.    
    
    5. Perform the Search Action  
        1. Simulate clicking the search trigger or execute the associated JavaScript action.  
        2. Handle page redirects or dynamically loaded results.
        3.Track the search state and retry if needed in case of failure.    
    
    6. Handle Search Results  
        1. Fetch updated HTML if results load on a new page or dynamically.
        2. Locate and document relevant links, text, or elements related to the search query ({Query}).
        3.Document results and save them for future reference.    
    
    7. Extract and Scrape Details  
        1. Parse the search results to extract details related to {Query}.  
        2. If further navigation is required (e.g., clicking a link), follow it and scrape additional details.
        3.Track the navigation for resumption in case of interruption.    
    
    8. Output the Results  
        1. Present the extracted information in a structured, readable text format.  
        2. Ensure the output is concise, accurate, and directly relevant to the query.    
    
    **Key Considerations**:  
        - **Dynamic Content**: Use automation tools to handle JavaScript or dynamically rendered elements.
        -**Unconventional Search Triggers:** Be ready to interact with elements that aren’t traditional buttons (like <a> tags with JavaScript functions).
        - **Unconventional Elements**: Account for hidden or icon-based buttons using heuristics. 
        - **Error Handling**: Implement robust error handling for missing or ambiguous elements, retrying or providing diagnostic reports.
        - **Optimization**: Minimize delays and interactions to ensure efficiency and reduce detection risks.
        -**State Persistence**: Save the state of the process to continue from where you left off in case of a re-run.
"""

user_proxy.initiate_chat(
    assistant,
    message=task
)