'''
Author: Maonan Wang
Date: 2025-04-09 10:43:14
LastEditTime: 2025-04-09 12:03:54
LastEditors: Maonan Wang
Description: 基于图片聊天机器人
FilePath: /llm_tutorial/QwenAgent-Tutorial/2_chatbot_image.py
'''
from qwen_agent.agents import Assistant
from qwen_agent.utils.utils import encode_image_as_base64
from qwen_agent.utils.output_beautify import typewriter_print


llm_cfg = {
    'model': 'Qwen/Qwen2.5-VL-32B-Instruct',
    'model_type': 'qwenvl_oai',
    'model_server': 'http://localhost:5003/v1',
    'api_key': 'token-abc123',

    # 模型配置参数
    'generate_cfg': {
        'top_p': 0.8,
    }
}

bot = Assistant(
    llm=llm_cfg,
    # system_message="你现在是一个图片描述机器人，给你一个图片，请你描述图片中的内容。",
)

messages = [] # This stores the chat history.
while True:
    text_query = input('\nuser query: ') # 输入问题
    image_query = input('Image Path: ')
    # 判断 Image Path 是否存在
    # Append the user query to the chat history.
    messages.append({
        'role': 'user', 
        'content':[
            {"text": text_query},
            {'image': image_query}
        ] # 多模态的输入
    })

    response = []
    response_plain_text = ''
    print('bot response:')
    for response in bot.run(messages=messages):
        response_plain_text = typewriter_print(response, response_plain_text)
    # Append the bot responses to the chat history.
    messages.extend(response) # 添加聊天历史