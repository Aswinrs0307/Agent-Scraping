import autogen
llm_config={
    "cache_seed": 1,  # change the seed for different trials
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
    code_execution_config={"work_dir":"Details","use_docker":False},
    llm_config=llm_config,
    system_message="""You are a web scraping agent and I need to scrape particular details from a web site """
)

url="https://efiling.drcor.mcit.gov.cy/DrcorPublic/SearchForm.aspx?sc=0&cultureInfo=en-AU"
Query="BANK OF CYPRUS PUBLIC COMPANY LIMITED"
task=f"""
    You are a web scraping agent tasked with scraping information from any provided URL . Your goal is to analyze the website's structure, extract the requested data efficiently, and return it in the desired format. From this website:{url}, you need to retrive the detail of **{Query}**. Once you scrape the web page then you should retrive the details of {Query} make the output in a **Text format**.
"""

user_proxy.initiate_chat(
    assistant,
    message=task
)