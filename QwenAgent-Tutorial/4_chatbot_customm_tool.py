'''
Author: Maonan Wang
Date: 2025-04-08 18:25:16
LastEditTime: 2025-04-25 17:50:52
LastEditors: Maonan Wang
Description: 在 Qwen 上添加自定义工具, 在启动 Model 的时候需要开启支持工具调用
CUDA_VISIBLE_DEVICES=1  vllm serve "Qwen/Qwen2.5-72B-Instruct-AWQ" --enable-auto-tool-choice --tool-call-parser hermes --dtype auto --api-key token-abc123 --port 5060
FilePath: /llm_tutorial/QwenAgent-Tutorial/4_chatbot_customm_tool.py
'''
import json5
from qwen_agent.agents import Assistant
from qwen_agent.tools.base import BaseTool, register_tool
from qwen_agent.utils.output_beautify import typewriter_print
from _config import llm_cfg

# Add a custom tools.
@register_tool('multiply')
class MultiplyTool(BaseTool):
    description = 'Multiply a and b.'
    parameters = [
        {
            'name': 'a',
            'type': 'int',
            'description': 'first int',
            'required': True
        },
        {
            'name': 'b',
            'type': 'int',
            'description': 'second int',
            'required': True
        }
    ]

    def call(self, params: str, **kwargs) -> int:
        input_params = json5.loads(params)
        a = input_params['a']
        b = input_params['b']
        print(f"INFO: 使用乘法工具, {a}*{b}.")
        return a * b


@register_tool('add')
class AddTool(BaseTool):
    description = 'Adds a and b.'
    parameters = [
        {
            'name': 'a',
            'type': 'int',
            'description': 'first int',
            'required': True
        },
        {
            'name': 'b',
            'type': 'int',
            'description': 'second int',
            'required': True
        }
    ]

    def call(self, params: str, **kwargs) -> int:
        input_params = json5.loads(params)
        a = input_params['a']
        b = input_params['b']
        print(f"INFO: 使用加法工具, {a}+{b}.")
        return a + b


@register_tool('divide')
class DivideTool(BaseTool):
    description = 'Divide a and b.'
    parameters = [
        {
            'name': 'a',
            'type': 'int',
            'description': 'first int',
            'required': True
        },
        {
            'name': 'b',
            'type': 'int',
            'description': 'second int',
            'required': True
        }
    ]

    def call(self, params: str, **kwargs) -> float:
        input_params = json5.loads(params)
        a = input_params['a']
        b = input_params['b']
        print(f"INFO: 使用除法工具, {a}/{b}.")
        return a / b


# 定义 Agent
system_instruction = '''现在你是一个小学数学老师，学生会问你一些简单的计算题，你需要首先给出答案（可以使用合适的工具进行计算），接着一步一步进行解释。'''
tools = ['multiply', 'add', 'divide']  # `code_interpreter` is a built-in tool for executing code.
bot = Assistant(
    llm=llm_cfg,
    system_message=system_instruction,
    function_list=tools,
)

# Run the agent as a chatbot.
messages = []  # This stores the chat history.
while True:
    # For example, enter the query "draw a dog and rotate it 90 degrees".
    query = input('\nuser query: ')
    # Append the user query to the chat history.
    messages.append({'role': 'user', 'content': query})
    response = []
    response_plain_text = ''
    print('bot response:')
    for response in bot.run(messages=messages):
        # Streaming output.
        response_plain_text = typewriter_print(response, response_plain_text)
    # Append the bot responses to the chat history.
    messages.extend(response)