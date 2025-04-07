'''
Author: Maonan Wang
Date: 2025-04-07 16:13:53
LastEditTime: 2025-04-07 16:37:28
LastEditors: Maonan Wang
Description: 本地部署 vLLM 后使用图片对话
FilePath: /llm_tutorial/LangChain-Tutorial/1_openai_api/c_openai_vllm_image.py
'''
import base64
from openai import OpenAI

def encode_image(image_path):
    """Encode the Image
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def ask_image_question(client, image_path, question):
    base64_image = encode_image(image_path)

    response = client.chat.completions.create(
        model="Qwen/Qwen2.5-VL-32B-Instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    },
                    {
                        "type": "text",
                        "text": question
                    }
                ]
            }
        ],
        max_tokens=300
    )

    return response.choices[0].message.content

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="token-abc123",
)


# Image
image_path = "/home/wmn/Github-Project/llm_tutorial/LangChain-Tutorial/1_openai_api/road_sim.png"
question = "是否可以告诉我道路上有多少车辆，是否存在特殊的车辆?"

answer = ask_image_question(client, image_path, question)
print(answer) 