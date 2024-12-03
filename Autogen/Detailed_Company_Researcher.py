import autogen



llm_config={
        # "timeout":600,
        "cache_seed":57,
        "config_list":autogen.config_list_from_json(
            env_or_file="OAI_CONFIG_LIST.json",
            filter_dict={
                "model":["Your API model"],
            }
        ),
        "temperature":0.3,
        "max_tokens":1000
}


assistant=autogen.AssistantAgent(
    name="Research_Assistant",
    llm_config=llm_config,
    system_message="You are a Company research Assistant . you have knowledge of Company all over the world."
)

user_proxy=autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode='TERMINATE',
    max_consecutive_auto_reply=5,
    is_termination_msg=lambda x:x.get("content"," ").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir":"Researcher","use_docker":False},
    llm_config=llm_config,
    system_message=""" Replay TERMINATE if the task has been solved at full satisfaction ,
    Otherwise,replay CONTINUE , or the reason why the task is not solved yet """

)

task="""Retrive and scrape  me some company related information from the url:https://www.hsagroup.com .You should go through the web site and retrive the details. 
    I need General information about company details i listed below:
        **Company Information Template:**
            - **Primary Business Address (Main):**
                    - [Enter the main business address here]

            - **Legal Form:**
                    - [Enter the legal form of the company here, e.g., Private Company, Public Company, etc.]

            - **Country:**
                    - [Enter the country where the company is registered]

            - **Town:**
                    - [Enter the town or city where the company is located]

            - **Registered Date:**
                    - [Enter the date when the company was registered]

            - **Registration Number:**
                    - [Enter the company's registration number]

            - **Phone:**
                    - (+967) (4) 215999

            - **Email:**
                    - [Enter the company's email address]

            - **Fax:**
                    - (+967) (4) 210584

            - **UBO (Ultimate Business Owners):**
                    - [Enter the names of the ultimate business owners]

            - **Directors/Shareholders:**
                    - [Enter the names of the directors and shareholders]

            - **Subsidiaries:**
                    - [List the company's subsidiaries]

            - **Parent Company:**
                    - [Enter the name of the parent company, if applicable]

            - **Last Reported Revenue:**
                    - [Enter the last reported revenue of the company]

        
        This is the detail I want to retrieve from the given url.And provide the details in this format.
    """

user_proxy.initiate_chat(
    assistant,
    message=task
)