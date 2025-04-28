'''
Author: Maonan Wang
Date: 2025-04-25 18:47:57
LastEditTime: 2025-04-28 14:29:55
LastEditors: Maonan Wang
Description: 存在一个 Host Agent 分配任务:
+ 存在一个 Agent 作图片理解
+ 如果存在特殊车辆, 则调用另外一个 Agent 思考逻辑
+ 如果不存在特殊车辆, 则返回专家决策 (这里返回的结果是固定值)
FilePath: /llm_tutorial/QwenAgent-Tutorial/8_group_agents.py
'''
from qwen_agent import Agent
from qwen_agent.agents import Assistant
from qwen_agent.agents import GroupChat
from qwen_agent.llm.schema import Message
from qwen_agent.utils.output_beautify import typewriter_print

from _config import llm_cfg, vlm_cfg

# 定义不同的 Agents
image_agent = Assistant(
    name='traffic scenario understanding',
    llm=vlm_cfg,
    system_message="你扮演一个在路口指挥交通的警察，你需要根据路口的情况，判断当前车道是否存在一些特殊车辆，例如警车，救护车或是消防车。" +\
        "如果存在特殊车辆，需要告诉我所在的车道，从左往右的序号。"
)

concer_case_decision_agent = Assistant(
    name='concer case decision agent',
    description='你扮演一个在路口指挥交通的警察，当路口存在特殊车辆，例如存在警车等情况需要你来决策。',
    llm=llm_cfg,
    system_message="你扮演一个在路口指挥交通的警察，你现在发现路口存在特殊车辆，例如存在警车等情况需要你来决策。请你根据当前车辆所在车道，给出决策。" +\
        "你需要在开头说一句：我是交警二。"
) 

class CustomAgent(Agent):
    def _run(self, messages, **kwargs):
        yield [Message(role='assistant', content="Phase-1", name=self.name)]
normal_case_decision_agent = CustomAgent(
    name='normal case decision agent',
    description='你扮演一个在路口指挥交通的警察，你只能在没有特殊车辆的时候给出决策。',
    system_message="你是在常规场景下给出决策的警察。"   
) 


# 创建 GroupChat
agents = [concer_case_decision_agent, normal_case_decision_agent]
group_bots = GroupChat(
    llm=llm_cfg, 
    agents=agents,
    agent_selection_method='auto',
)



while True:
    messages = []  # 每一轮对话都是独立的

    # 场景分析 (分析场景图片)
    text_query = '请你仔细分析下面的场景，是否包含特殊车辆。' # 输入问题
    image_query = input('\nImage Path: ') # 场景图片

    content = [{"text": text_query}]
    content.append({'image': image_query})

    messages.append({
        'role': 'user',
        'content': content  # 多模态的输入
    })  # Append the user query to the chat history.

    print('\n-->Image Bot Response:<--')
    response = []
    response_plain_text = ''
    for response in image_agent.run(messages=messages):
        response_plain_text = typewriter_print(response, response_plain_text)

    # 不同场景进行不同决策
    messages = [] # 重新构造对话历史
    messages.append({
        'role': 'user',
        'content': '请你根据当前的交通路口状态做出决策。'  # 多模态的输入
    })  # Append the user query to the chat history.
    messages.extend(response)  # 添加聊天历史 (决策 bots 需要参考当前场景分析)
    
    print('\n-->Group Bots Response:<--')
    response = []
    response_plain_text = ''
    for response in group_bots.run(messages=messages, max_round=1):
        response_plain_text = typewriter_print(response, response_plain_text)