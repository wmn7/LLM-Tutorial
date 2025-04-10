'''
Author: Maonan Wang
Date: 2025-04-10 14:48:54
LastEditTime: 2025-04-10 14:55:13
LastEditors: Maonan Wang
Description: 聊天机器人, 只有 3 轮的记忆, 下面是一个例子

```
Input: user query: 你好,我的名字是xxx,希望你可以记住
Output: bot response: 你好，xxx！很高兴认识你，我会记住你的名字的。有什么我可以帮你的吗？😊
Input: user query: 告诉我1+10 的结果
Output: bot response: 1 + 10 = **11** 😊
Input: user query: 告诉我2*9的结果
Output: bot response: 2 × 9 = **18** 😊
Input: user query: 告诉我 10*10 的结果
Output: bot response: 10 × 10 = **100** 😊
Input: user query: 我的名字叫什么
Output: bot response: 你好呀！你没有告诉我你的名字呢，可以和我分享一下吗？😊
```

FilePath: /llm_tutorial/QwenAgent-Tutorial/2_chatbot_text_without_memory.py
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