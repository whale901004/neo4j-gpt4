import os
import openai

openai.api_key = "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"

system = f"""
您是一個協助回答疾病相關問題的助手。
最新的提示包含了相關信息，您需要基於提供的信息生成人類可理解的回答。
請讓回答聽起來像是來自AI助手，但不要添加任何多餘的信息。
請勿添加任何未在最新提示中明確提供的額外信息。
我再次強調，請勿添加任何未明確給出的信息。
"""

def generate_response(messages):
    messages = [
        {"role": "system", "content": system}
    ] + messages
    print(messages)
    # Make a request to OpenAI
    completions = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.0
    )
    response = completions.choices[0].message.content
    print(response)
    # If the model apologized, remove the first line or sentence
    if "apologi" in response:
        if "\n" in response:
            response = " ".join(response.split("\n")[1:])
        else:
            response = " ".join(response.split(".")[1:])
    return response


if __name__ == '__main__':
    data = [{'disease': '感冒', 'symptom': "流鼻涕"}, {'disease': '偏頭痛', "symptom": "頭痛"}, {
        'disease': '肺膿腫'}, {'disease': '肺炎'}]
    print(generate_response([{'role': 'user', 'content': str(data)}]))

