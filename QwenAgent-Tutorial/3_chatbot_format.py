'''
Author: Maonan Wang
Date: 2025-04-25 17:16:17
LastEditTime: 2025-04-25 17:32:02
LastEditors: Maonan Wang
Description: LLM 输出为 JSON 格式
FilePath: /llm_tutorial/QwenAgent-Tutorial/3_chatbot_format.py
'''
import json
from qwen_agent.agents import Assistant
from qwen_agent.utils.output_beautify import typewriter_print
from _config import llm_cfg

llm_cfg['generate_cfg']['response_format'] = {"type": "json_object"}
print(llm_cfg)
"""完整的配置文件如下所示:
llm_cfg = {
    'model': 'Qwen/Qwen2.5-72B-Instruct-AWQ',
    'model_type': 'oai',
    'model_server': 'http://localhost:5060/v1',
    'api_key': 'token-abc123',

    # 模型配置参数
    'generate_cfg': {
        'top_p': 0.8,
        'response_format': {"type": "json_object"},
    }
}
"""

example_response = json.dumps(
    {
        "Answer": "12*11=132",
        "Explanation": "可以理解为12个11相加，或者11个12相加。"
    },
    ensure_ascii=False
)

_system_message = (
    f"现在你是一个数学机器人，用户问你数学问题，你回答答案并进行解释。你需要使用 JSON 格式回答，包含两个 key，分别是 Answer 包含答案，和 Explanation 为解释。"
    f"例如用户询问 12*11，你需要回答 \n{example_response}"
)
bot = Assistant(
    llm=llm_cfg,
    system_message=_system_message,
    
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