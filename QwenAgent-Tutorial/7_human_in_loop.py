'''
Author: Maonan Wang
Date: 2025-04-10 16:36:30
LastEditTime: 2025-04-25 18:01:35
LastEditors: Maonan Wang
Description: 加入一个人类参与的 Agents
FilePath: /llm_tutorial/QwenAgent-Tutorial/7_human_in_loop.py
'''
import copy
from typing import Dict, Iterator, List, Optional, Union

from qwen_agent import Agent
from qwen_agent.agents import Assistant
from qwen_agent.tools import BaseTool
from qwen_agent.tools.base import BaseTool, register_tool
from qwen_agent.llm.schema import ContentItem, Message
from qwen_agent.utils.output_beautify import typewriter_print
from _config import llm_cfg, vlm_cfg

@register_tool('tsc_expert_decision')
class ExpertDecisionTool(BaseTool):
    description = '常规交通场景下的专家策略，常规场景下情参考该工具的结果。'
    def call(self, params: str, **kwargs) -> int:
        return "Switch to Phase-1."

@register_tool('human_in_loop')
class HumanInLoop(BaseTool):
    description = '特殊情况下让人工介入。'
    def call(self, params: str, **kwargs) -> int:
        message = input("人工的建议: ")
        return message


class TSCDecision(Agent):
    """Customize an agent for make decision according to the image"""

    def __init__(self,
            llm_cfg: Dict = None, vlm_cfg: Dict = None, 
            function_list: Optional[List[Union[str, Dict, BaseTool]]] = None,
            
        ):
        super().__init__()

        # Nest one vl assistant for image understanding
        self.image_agent = Assistant(
            llm=vlm_cfg,
            system_message="你扮演一个在路口指挥交通的警察，你需要根据路口的情况，判断当前车道是否存在一些特殊车辆，例如警车，救护车或是消防车。" +\
                "如果存在特殊车辆，需要告诉我所在的车道，从左往右的序号。"
        )

        # Nest one assistant for making decision
        self.decision_agent = Assistant(
            llm=llm_cfg,
            function_list=function_list,
            system_message='你扮演一个在路口指挥交通的警察，根据当前路口情况进行决策。' + \
                '如果当前路口没有特殊情况，则参考专家的建议，也就是工具 tsc_expert_decision；' + \
                '如果存在特殊车辆，则应该希望人工介入，也就是调用工具 human_in_loop。'
            )


    def _run(self, messages: List[Message], lang: str = 'zh', **kwargs) -> Iterator[List[Message]]:
        """Define the workflow
        """
        assert isinstance(messages[-1]['content'], list)
        assert any([item.image for item in messages[-1]['content']]), 'This agent requires input of images'

        # Image understanding
        new_messages = copy.deepcopy(messages) # 上下文记忆
        new_messages[-1]['content'].append(ContentItem(text='这是一个路口某个方向的摄像头图片，请你仔细观察该路口是否包含特殊车辆，还是常规场景。如果存在特殊车辆，告诉我所在的车道。'))
        response = []
        for rsp in self.image_agent.run(new_messages):
            yield response + rsp
        response.extend(rsp)
        new_messages.extend(rsp)

        # Decision Making
        new_messages.append(
            Message(
                'user', 
                [ContentItem(text='请你根据当前的场景来做出决策：常规场景参考专家策略；特殊场景不需要参考专家策略。')]
            ))
        for rsp in self.decision_agent.run(new_messages, lang=lang, **kwargs):
            yield response + rsp
        


def app_tui():
    bot = TSCDecision(
        llm_cfg=llm_cfg, vlm_cfg=vlm_cfg,
        function_list=['tsc_expert_decision', 'human_in_loop']
    )

    # Chat
    while True:
        messages = [] # 每一轮对话处理一张图
        image = input('\nimage path: ').strip()
        messages.append(Message('user', [ContentItem(image=image)])) # 传入的图片

        response = []
        response_plain_text = "" # 为了可视化
        for response in bot.run(messages):
            response_plain_text = typewriter_print(response, response_plain_text)
        messages.extend(response)


if __name__ == '__main__':
    app_tui()