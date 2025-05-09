'''
Author: Maonan Wang
Date: 2025-04-09 10:43:14
LastEditTime: 2025-04-25 17:39:28
LastEditors: Maonan Wang
Description: 基于图片聊天机器人
FilePath: /llm_tutorial/QwenAgent-Tutorial/4_chatbot_image.py
'''
import os
from qwen_agent.agents import Assistant
from qwen_agent.utils.output_beautify import typewriter_print

from _config import vlm_cfg

bot = Assistant(
    llm=vlm_cfg,
    system_message="你现在是一个图片描述机器人，给你一个图片，请你描述图片中的内容。",
)

messages = []  # This stores the chat history.
has_image = False  # 标记是否已经有图片

while True:
    text_query = input('\nuser query: ')  # 输入问题
    image_query = input('Image Path: ')

    # 判断是否每一轮都输入图片, 没有图片输出只有纯文本
    content = [{"text": text_query}]
    if os.path.exists(image_query):
        if has_image:
            # 如果已经有图片，删除之前的聊天记录
            messages = []
        has_image = True
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
    messages.extend(response)  # 添加聊天历史