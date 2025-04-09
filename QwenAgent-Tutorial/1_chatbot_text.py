'''
Author: Maonan Wang
Date: 2025-04-09 10:42:48
LastEditTime: 2025-04-09 10:50:46
LastEditors: Maonan Wang
Description: 基于文本的聊天机器人
FilePath: /llm_tutorial/QwenAgent-Tutorial/1_chatbot_text.py
'''
from qwen_agent.agents import Assistant
from qwen_agent.utils.output_beautify import typewriter_print


llm_cfg = {
    'model': 'Qwen/Qwen2.5-VL-32B-Instruct',
    'model_server': 'http://localhost:5003/v1',
    'api_key': 'token-abc123',

    # 模型配置参数
    'generate_cfg': {
        'top_p': 0.8,
    }
}

bot = Assistant(
    llm=llm_cfg,
    system_message="现在你是一个复读机，用户输入什么，你就重复什么。",
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
    messages.extend(response)