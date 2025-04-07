'''
Author: Maonan Wang
Date: 2025-04-07 15:58:14
LastEditTime: 2025-04-07 18:55:16
LastEditors: Maonan Wang
Description: 组合 Prompt 进行翻译任务 (风格转换)
FilePath: /llm_tutorial/LangChain-Tutorial/1_openai_api/c_openai_difficulty_task.py
'''
from openai import OpenAI

def get_completion(prompt, model="Qwen/Qwen2.5-VL-32B-Instruct"):
    client = OpenAI(
        base_url="http://localhost:8000/v1",
        api_key="token-abc123",
    )
    
    messages = [{"role": "user", "content": prompt}]
    
    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0, 
    )
    return completion.choices[0].message.content

if __name__ == '__main__':
    # 原始的信息
    customer_email = """
    Arrr, I be fuming that me blender lid \
    flew off and splattered me kitchen walls \
    with smoothie! And to make matters worse,\
    the warranty don't cover the cost of \
    cleaning up me kitchen. I need yer help \
    right now, matey!
    """

    # 美式英语 + 平静、尊敬的语调
    style = """American English \
    in a calm and respectful tone, at last translate to Simplified Chinese
    """

    # 要求模型根据给出的语调进行转化 (构建 prompt)
    prompt = f"""Translate the text \
    that is delimited by triple backticks 
    into a style that is {style}.
    text: ```{customer_email}```
    """

    # 传入模型获得回答
    answer = get_completion(prompt)
    print(answer)