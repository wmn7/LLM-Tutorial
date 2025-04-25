'''
Author: Maonan Wang
Date: 2025-04-09 10:42:48
LastEditTime: 2025-04-25 17:07:48
LastEditors: Maonan Wang
Description: 基于文本的聊天机器人 (没有记忆)
FilePath: /llm_tutorial/QwenAgent-Tutorial/1_chatbot_text.py
'''
from qwen_agent.agents import Assistant
from qwen_agent.utils.output_beautify import typewriter_print

from _config import llm_cfg

bot = Assistant(
    llm=llm_cfg,
    system_message="现在你是一个聊天机器人，请你使用简短的语言进行聊天。",
)


while True:
    messages = []  # This stores the chat history.
    query = input('\nuser query: ') # 输入问题
    # Append the user query to the chat history.
    messages.append({'role': 'user', 'content': query})
    response = []
    response_plain_text = ''
    print('bot response:')
    for response in bot.run(messages=messages):
        response_plain_text = typewriter_print(response, response_plain_text)