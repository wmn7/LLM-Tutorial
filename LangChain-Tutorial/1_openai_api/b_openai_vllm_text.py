'''
Author: Maonan Wang
Date: 2025-04-07 16:00:45
LastEditTime: 2025-04-07 16:03:58
LastEditors: Maonan Wang
Description: 本地部署 vLLM 后纯文本对话, 调用 OpenAI 对本地模型进行调用
FilePath: /llm_tutorial/LangChain-Tutorial/1_openai_api/b_openai_vllm_text.py
'''
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="token-abc123",
)

# Text
completion = client.chat.completions.create(
  model="Qwen/Qwen2.5-VL-32B-Instruct",
  messages=[
    {"role": "user", "content": "Can you tell me what is 3 plus 8 step by step?"}
  ]
)

print(completion.choices[0].message)