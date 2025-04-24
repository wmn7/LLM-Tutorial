'''
Author: Maonan Wang
Date: 2025-04-24 20:16:50
LastEditTime: 2025-04-24 20:16:52
LastEditors: Maonan Wang
Description: LLM 服务配置
FilePath: /llm_tutorial/QwenAgent-Tutorial/_config.py
'''
llm_cfg = {
    'model': 'Qwen/Qwen2.5-7B-Instruct',
    'model_type': 'oai',
    'model_server': 'http://localhost:5010/v1',
    'api_key': 'token-abc123',

    'generate_cfg': {
        'top_p': 0.8,
    }
}

vlm_cfg = {
    'model': 'Qwen/Qwen2.5-VL-32B-Instruct-AWQ',
    'model_type': 'qwenvl_oai',
    'model_server': 'http://localhost:5030/v1',
    'api_key': 'token-abc123',

    'generate_cfg': {
        'top_p': 0.8,
    }
}