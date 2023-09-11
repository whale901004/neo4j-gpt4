import os
import openai
from retry import retry

from training import examples

openai.api_key = "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"

system = f"""
您是一名助手，可以根據示例Cypher查詢生成Cypher查詢。
示例Cypher查詢如下： \n {examples} \n
除了Cypher查詢之外，不要回應任何解釋或其他信息。
您不需要道歉，只需嚴格根據提供的Cypher示例生成Cypher語句。
當使用者提到關於疾病相關的內容時，您需要使用適當的 Cypher 語句更新數據庫。
在無法推斷出Cypher語句的情況下，請告知使用者，因為對話缺乏上下文，並說明缺少的上下文是什麼。
"""


@retry(tries=2, delay=5)
def generate_cypher(messages):
    messages = [
        {"role": "system", "content": system}
    ] + messages
    print(messages)
    # 向 OpenAI 發出請求
    completions = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.0
    )
    response = completions.choices[0].message.content
    # 有時模型會繞過系統提示並返回
    # 基於之前對話歷史的數據
    if not "MATCH" in response and "{" in response:
        raise Exception(
            "GPT bypassed system message and is returning response based on previous conversation history" + response)
    # 如果模型道歉了，刪除第一行
    if "apologi" in response:
        response = " ".join(response.split("\n")[1:])
    # 有時，當模型想要解釋某些內容時，它會在 Cypher 周圍添加引號
    if "`" in response:
        response = response.split("```")[1].strip("`")
    print(response)
    return response


if __name__ == '__main__':
    print(generate_cypher([{'role': 'user', 'content': '最近一直流鼻涕怎麼辦？'},
                           {'role': 'assistant', 'content': '流鼻涕可能是感冒的症狀，建議休息並多喝水。'},
                           {'role': 'user','content': '感冒的症狀有什麼？'}
                           ]))
    print(generate_cypher([{'role': 'user', 'content': '最近一直流鼻涕怎麼辦？'},
                           {'role': 'assistant', 'content': '流鼻涕可能是感冒的症狀，建議休息並多喝水。'},
                           {'role': 'user','content': '耳鳴的話吃甚麼可以改善？'}]))
