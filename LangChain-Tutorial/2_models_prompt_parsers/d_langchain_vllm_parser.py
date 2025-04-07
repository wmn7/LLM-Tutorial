'''
Author: Maonan Wang
Date: 2025-04-07 15:58:14
LastEditTime: 2025-04-07 19:45:29
LastEditors: Maonan Wang
Description: 提取文本中的信息, 按照指定的格式进行输出 (这里输出为 dict)
FilePath: /llm_tutorial/LangChain-Tutorial/2_models_prompt_parsers/c_langchain_vllm_parser.py
'''
from langchain_community.llms import VLLMOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

customer_review = """\
This leaf blower is pretty amazing. It has four settings:\
candle blower, gentle breeze, windy city, and tornado. \
It arrived in two days, just in time for my wife's \
anniversary present. \
I think my wife liked it so much she was speechless. \
So far I've been the only one using it, and I've been \
using it every other morning to clear the leaves on our lawn. \
It's slightly more expensive than the other leaf blowers \
out there, but I think it's worth it for the extra features. \
"""

review_template = """\
For the following text, extract the following information:

gift: Was the item purchased as a gift for someone else? \
Answer True if yes, False if not or unknown.

delivery_days: How many days did it take for the product \
to arrive? If this information is not found, output -1.

price_value: Extract any sentences about the value or price,\
and output them as a comma separated Python list. \

text: {text}

{format_instructions}
"""

if __name__ == '__main__':
    # 模型初始化
    llm = VLLMOpenAI(
        openai_api_key="token-abc123",
        openai_api_base="http://localhost:8000/v1",
        model_name="Qwen/Qwen2.5-VL-32B-Instruct",
    )

    # #################
    # 构造 parser 的模板 (1.构造格式化输出; 2.构造 Prompt)
    # #################
    gift_schema = ResponseSchema(
        name="gift",
        description="Was the item purchased as a gift for someone else? \
                    Answer True if yes, False if not or unknown.")

    delivery_days_schema = ResponseSchema(
        name="delivery_days",
        description="How many days did it take for the product= to arrive? \
            If this information is not found, output -1.")
    
    price_value_schema = ResponseSchema(
        name="price_value",
        description="Extract any sentences about the value or price, \
            and output them as a comma separated Python list.")

    response_schemas = [
        gift_schema, 
        delivery_days_schema,
        price_value_schema
    ]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions() # 转换为提示词

    # Input 模板 (这个模板可以传入不同的参数进行重复使用)
    prompt_templete = ChatPromptTemplate.from_template(review_template)
    custom_message = prompt_templete.format_messages(
        text = customer_review, # 查询的内容
        format_instructions = format_instructions # 将输出的格式要求作为 prompt 的一部分
    )
    print(custom_message[0].content) # 构建好的 message 的内容

    # #############
    # 将 prompt 传入 chat 进行问答
    # #############
    custom_response = llm.invoke(custom_message)
    print(f'原始回复:\n{custom_response}')
    output_dict = output_parser.parse(custom_response)
    print(f'格式化后回复:\n 格式: {type(output_dict)}; \n 回复: {output_dict}') # 此时转换为 dict