import autogen

llm_config={
        # "timeout":600,
        "cache_seed":59,
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
    name="Assistant",
    llm_config=llm_config,
)

user_proxy=autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode='TERMINATE',
    max_consecutive_auto_reply=5,
    is_termination_msg=lambda x:x.get("content"," ").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir":"date_time","use_docker":False},
    llm_config=llm_config,
    system_message=""" Replay TERMINATE if the task has been solved at full satisfaction ,
    Otherwise,replay CONTINUE , or the reason why the task is not solved yet """

)

task="""what is the date today? and give a python code for that and check that this year is leap year or not.And try to get the information of today gold rate in tamil nadu"""

user_proxy.initiate_chat(
    assistant,
    message=task
)