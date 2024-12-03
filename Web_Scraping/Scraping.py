import autogen
llm_config={
    "cache_seed": 3,  # change the seed for different trials
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
    code_execution_config={"work_dir":"Web_Scraping","use_docker":False},
    llm_config=llm_config,
    system_message="""You are a web scraping agent and I need to scrape particular details from a web site """
)

url="https://efiling.drcor.mcit.gov.cy/DrcorPublic/SearchForm.aspx?sc=0&cultureInfo=en-AU"
Query="BANK OF CYPRUS PUBLIC COMPANY LIMITED"
task=f"""
    You are a web scraping agent tasked with scraping information from any provided URL . Your goal is to analyze the website's structure, extract the requested data efficiently, and return it in the desired format. From this website:{url}, you need to scrap the HTML content and try to get all ID , names and Classname of a text field for searching input and then try to give the user {Query} .Here the user can give any input that will be a name or ID as a input as {Query}.next try to scrape the button used in this web site,there is a onclick button ,it could be in any name.once you find the button field and then click the respected button for searching. if the search result will open another link then also extract that HTML content then look for the expected result.if this search result provide any link related to that {Query} then extract it and open that link.then scrape that link and find the details related to the input provided {Query}.Lastly , retrive the detail of **{Query}**. Once you scrape the web page then you should retrive the details of {Query} make the output in a **Text format**.
"""

user_proxy.initiate_chat(
    assistant,
    message=task
)