import autogen
llm_config={
    "cache_seed": 46,  # change the seed for different trials
    "config_list": autogen.config_list_from_json(
        "OAI_CONFIG_LIST.json",
        filter_dict={"model": ["Your API model"]},
    ),
    "temperature": 0.3,
    "max_tokens":1000
}

assistant=autogen.AssistantAgent(
    name="Web Scraping Agent",
    llm_config=llm_config
)

user_proxy=autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode='TERMINATE',
    max_consecutive_auto_reply=5,
    is_termination_msg=lambda x:x.get("content"," ").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir":"Scraping","use_docker":False},
    llm_config=llm_config,
    system_message="""You are a web scraping agent and i need to scrape particular details from a web site """
)

url="https://efiling.drcor.mcit.gov.cy/DrcorPublic/?cultureInfo=en-AU"
task=f"""
    You are Expertise in Web Scrapping. Your task is to extract the required the data from the given site {url}. 
    Follow the steps given below to extract the informations.
    **Important Steps**:
    1. Go to the url.
    2. Navigate to the search option and go to that url.
    3. In Search url there is Search Criteria choose "with all these words".
    4. In Name type "jack" and there is another input lable as Reg no leave as empty.
    5. Then Click "Go" button.
    6. Once the "Go" button is clicked In the below of that there will be many links will appear.
    7.select the first link , if you select the first link it will take you to another page where that particular person details will be available.
    8. In that table Extract the Datas in the columns "Name", "Reg. Number", "Type", "Name Status", "Organisation Status".
    9. return this informations as a response.
    10. I need You to retrive the detail of the mentioned name from that web site and give the output in JSON format.
"""

user_proxy.initiate_chat(
    assistant,
    message=task
)