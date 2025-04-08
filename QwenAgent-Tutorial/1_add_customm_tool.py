'''
Author: Maonan Wang
Date: 2025-04-08 18:25:16
LastEditTime: 2025-04-08 18:43:52
LastEditors: Maonan Wang
Description: 在 Qwen 上添加自定义工具
FilePath: /llm_tutorial/QwenAgent-Tutorial/1_add_customm_tool.py
'''
import json5
from qwen_agent.agents import Assistant
from qwen_agent.tools.base import BaseTool, register_tool
from qwen_agent.utils.output_beautify import typewriter_print


# Step 1 (Optional): Add a custom tools.
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


# Step 2: Configure the LLM you are using.
llm_cfg = {
    # Use a model service compatible with the OpenAI API, such as vLLM or Ollama:
    'model': 'Qwen/Qwen2.5-VL-32B-Instruct',
    'model_server': 'http://localhost:8000/v1',  # base_url, also known as api_base
    'api_key': 'token-abc123',

    # (Optional) LLM hyperparameters for generation:
    'generate_cfg': {
        'top_p': 0.8
    }
}

# Step 3: Create an agent. Here we use the `Assistant` agent as an example, which is capable of using tools and reading files.
system_instruction = '''现在你是一个小学数学老师，学生会问你一些简单的计算题，你需要首先给出答案，接着一步一步进行解释:'''
tools = ['multiply', 'add', 'divide']  # `code_interpreter` is a built-in tool for executing code.
bot = Assistant(
    llm=llm_cfg,
    system_message=system_instruction,
    function_list=tools,
)

# Step 4: Run the agent as a chatbot.
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