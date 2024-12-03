import autogen


def autogen_configuration():
    llm_config = {
        # "timeout": 600,
        "cache_seed": 60,  # change the seed for different trials
        "config_list": autogen.config_list_from_json(
            "OAI_CONFIG_LIST.json",
            filter_dict={"model": ["Your API model"]},
        ),
        "temperature": 0,
        "max_tokens": 1000
    }
    return llm_config


def autogen_assistant(**kwargs):
    assistant = autogen.AssistantAgent(
        name=kwargs['assistant_name'],
        system_message=kwargs['assistant_sys_msg'],
        llm_config=kwargs['llm_config'],
    )
    return assistant


def autogen_agent(**kwargs):
    llm_config = autogen_configuration()

    user_proxy = autogen.UserProxyAgent(
        name=kwargs['agent_name'],
        human_input_mode="NEVER",
        system_message=kwargs['agent_sys_message'],
        max_consecutive_auto_reply=5,
        code_execution_config={
            "work_dir": "work_dir",
            "use_docker": False,
        },
        llm_config=llm_config
    )
    return user_proxy


def user_questions(**kwargs):
    assistant = autogen_assistant(assistant_name=kwargs['assistant_name'],assistant_sys_msg=kwargs['assistant_sys_msg'],llm_config=kwargs['llm_config'])

    proxy_agent = autogen_agent(agent_name=kwargs['agent_name'], agent_sys_message=kwargs['agent_sys_message'])

    response = proxy_agent.initiate_chat(assistant, message=kwargs['prompt'])
    return response


def user_prompt(path):
    with open(path, 'r') as r:
        prompt = r.read()
    return prompt


def autogen_main(**kwargs):
    llm_config = autogen_configuration()

    assistant_name = kwargs['assistant_name']
    assistant_sys_msg = kwargs['assistant_sys_msg']
    llm_config = llm_config

    agent_name = kwargs['agent_name']
    agent_sys_message = kwargs['agent_sys_message']
    prompt_concat = kwargs['prompt']
    agent_response = user_questions(assistant_name=assistant_name,
                                    assistant_sys_msg=assistant_sys_msg,
                                    llm_config=llm_config,
                                    agent_name=agent_name,
                                    agent_sys_message=agent_sys_message,
                                    prompt=prompt_concat)
    return agent_response.chat_history[-1]['content']

prompt_path=r'prompt.txt'
new_prompt=user_prompt(prompt_path)
url='https://efiling.drcor.mcit.gov.cy/'
input_content = f"{new_prompt}\n\n<Url>:\n\n{url}"


autogen_main(assistant_name="Web_crawling_Assistant",
        assistant_sys_msg="You are a helpful web crawling assistant you can find what I expect",
        agent_name="web_crawling_Agent",
        agent_sys_message="You are expertise in Web crawling so you can help me in extracting expected content from the web page.",
        prompt=input_content
)