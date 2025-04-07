'''
Author: Maonan Wang
Date: 2025-04-07 15:58:14
LastEditTime: 2025-04-07 19:58:01
LastEditors: Maonan Wang
Description: 使用 Langchain 的 Prompt 模板, 使用 ChatOpenAI 的方式
FilePath: /llm_tutorial/LangChain-Tutorial/2_models_prompt_parsers/a_langchain_openai_prompt.py
'''
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

customer_email = """
Arrr, I be fuming that me blender lid \
flew off and splattered me kitchen walls \
with smoothie! And to make matters worse,\
the warranty don't cover the cost of \
cleaning up me kitchen. I need yer help \
right now, matey! \
"""

custom_style = """American English \
in a calm and respectful tone, at last translate to Simplified Chinese. \
"""

if __name__ == '__main__':
    # 模型初始化
    chat = ChatOpenAI(
        model='Qwen/Qwen2.5-VL-32B-Instruct', 
        openai_api_key="token-abc123", 
        openai_api_base="http://localhost:8000/v1",
    )

    # 创建模板 (这个模板可以传入不同的参数进行重复使用)
    template_string = (
        "Translate the text that is delimited by triple backticks "
        "into a style that is {style}"
        "text: \n```{text}\n```"
    )
    prompt_templete = ChatPromptTemplate.from_template(template_string)
    # 传入不同的参数
    custom_message = prompt_templete.format_messages(
        style = custom_style,
        text = customer_email
    ) # 构造 Prompt
    
    # ###################
    # 将 prompt 传入 chat
    # ###################
    print(f'1. 传入的信息:\n{custom_message}')
    custom_response = chat.invoke(custom_message) # 进行提问
    print(f'2. 回答的结果:\n{custom_response}')