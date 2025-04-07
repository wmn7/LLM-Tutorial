'''
@Author: WANG Maonan
@Date: 2023-09-04 14:22:23
@Description: 使用 openai 进行问答, 使用 ChatGPT 官方接口 
LastEditTime: 2025-04-07 16:40:05
'''
import openai

def get_completion(prompt, model="gpt-3.5-turbo"):
    
    messages = [{"role": "user", "content": prompt}]
    
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, 
    )
    return response.choices[0].message["content"]

if __name__ == '__main__':
    openai.proxy = "http://127.0.0.1:7890"
    openai.api_key = "xxx"
    print(get_completion('Can you tell me what is 3 plus 8 step by step.'))