'''
Author: Maonan Wang
Date: 2025-04-07 19:47:09
LastEditTime: 2025-04-07 20:15:10
LastEditors: Maonan Wang
Description: 使用 LangChain 输入图片, 结合 Prompt
FilePath: /llm_tutorial/LangChain-Tutorial/2_models_prompt_parsers/c_langchain_vllm_image.py
'''
import base64
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate


def local_image_to_data_url(image_path):
    # Read and encode the image file
    with open(image_path, "rb") as image_file:
        base64_encoded_data = base64.b64encode(image_file.read()).decode('utf-8')

    # Construct the data URL
    return f"data:image/png;base64,{base64_encoded_data}"

if __name__ == '__main__':
    # 模型初始化
    chat = ChatOpenAI(
        model='Qwen/Qwen2.5-VL-32B-Instruct', 
        openai_api_key="token-abc123", 
        openai_api_base="http://localhost:8000/v1",
    )

    # 创建模板 (这个模板可以传入不同的参数进行重复使用)
    prompt_template = [
        SystemMessage(content="是否可以告诉我道路上有多少车辆，是否存在特殊的车辆?"),
        HumanMessagePromptTemplate.from_template(
            template=[
                {
                    "type": "image_url",
                    "image_url": "{encoded_image_url}",
                },
            ])
        ]

    summarize_image_prompt = ChatPromptTemplate.from_messages(prompt_template)
    # 传入不同的参数
    page3_encoded = local_image_to_data_url("../../assets/road_sim.png") # 图片编码
    custom_message = summarize_image_prompt.format_messages(
        encoded_image_url = page3_encoded,
    ) # 构造 Prompt

    # ###################
    # 将 prompt 传入 chat
    # ###################
    custom_response = chat.invoke(custom_message) # 进行提问
    print(custom_response.content)
