import autogen
llm_config={
    "cache_seed": 58,  # change the seed for different trials
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
    code_execution_config={"work_dir":"Test","use_docker":False},
    llm_config=llm_config,
    system_message="""You are a web scraping agent and i need to scrape particular details from a web site """
)

url="https://whed.net/home.php#:~:text=World%20Higher%20Education%20Database%20(WHED)%20Portal"
task=f"""
    scrape this web page and retrive the details and look for List of IAU Members Organizations and click that link and inside that link look for search put search input as medical and select go to view the data and retrive the first data from the search result this website:{url} .Once retrive the information make the output in a **Text file**.
"""

user_proxy.initiate_chat(
    assistant,
    message=task
)