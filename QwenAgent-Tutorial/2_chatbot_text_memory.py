'''
Author: Maonan Wang
Date: 2025-04-10 14:48:54
LastEditTime: 2025-04-25 17:13:07
LastEditors: Maonan Wang
Description: 聊天机器人, 只有 3 轮的记忆, 下面是一个例子
FilePath: /llm_tutorial/QwenAgent-Tutorial/2_chatbot_text_memory.py
'''
from qwen_agent.agents import Assistant
from qwen_agent.utils.output_beautify import typewriter_print
from _config import llm_cfg

bot = Assistant(
    llm=llm_cfg,
    system_message="现在你是一个聊天机器人，请你使用简短的语言进行聊天。",
)

messages = []  # This stores the chat history.
while True:
    query = input('\nuser query: ') # 输入问题
    # Append the user query to the chat history.
    messages.append({'role': 'user', 'content': query})
    response = []
    response_plain_text = ''
    print('bot response:')
    for response in bot.run(messages=messages):
        response_plain_text = typewriter_print(response, response_plain_text)
    # Append the bot responses to the chat history.
    messages.extend(response) # 添加聊天历史

    # 只保留最近的三轮对话（6 条消息）
    if len(messages) > 6:
        messages = messages[-6:]