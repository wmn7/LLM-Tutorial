'''
Author: Maonan Wang
Date: 2025-04-09 10:43:14
LastEditTime: 2025-04-23 18:21:34
LastEditors: Maonan Wang
Description: 基于图片聊天机器人
FilePath: /llm_tutorial/QwenAgent-Tutorial/3_chatbot_image.py
'''
import os
from qwen_agent.agents import Assistant
from qwen_agent.utils.output_beautify import typewriter_print

llm_cfg = {
    'model': 'Qwen/Qwen2.5-VL-32B-Instruct-AWQ',
    'model_type': 'qwenvl_oai',
    'model_server': 'http://localhost:5030/v1',
    'api_key': 'token-abc123',

    # 模型配置参数
    'generate_cfg': {
        'top_p': 0.8,
    }
}


bot = Assistant(
    llm=llm_cfg,
    system_message="你现在是一个图片描述机器人，给你一个图片，请你描述图片中的内容。",
)

messages = [] # This stores the chat history.
while True:
    text_query = input('\nuser query: ') # 输入问题
    image_query = input('Image Path: ')

    # 判断是否每一轮都输入图片
    content = [{"text": text_query}]
    if os.path.exists(image_query):
        content.append({'image': image_query})

    messages.append({
        'role': 'user',
        'content': content  # 多模态的输入
    })  # Append the user query to the chat history.

    response = []
    response_plain_text = ''
    print('bot response:')
    for response in bot.run(messages=messages):
        response_plain_text = typewriter_print(response, response_plain_text)
    # Append the bot responses to the chat history.
    messages.extend(response) # 添加聊天历史