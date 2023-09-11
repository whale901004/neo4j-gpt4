
import os
import openai
import streamlit as st
from streamlit_chat import message

from neo4j_driver import run_query
from english2cypher import generate_cypher
from graph2text import generate_response

# Hardcoded UserID
USER_ID = "Cindy"

# 第一次執行時，我們必須在數據庫中創建一個用戶節點。
run_query("""
MERGE (u:User {id: $userId})
""", {'userId': USER_ID})

st.set_page_config(layout="wide")
st.title("NeoGPT with context : GPT-4 + Neo4j")


def generate_context(prompt, context_data='generated'):
    context = []
    # 如果存在任何歷史記錄
    if st.session_state['generated']:
        # 添加最後三個交換
        size = len(st.session_state['generated'])
        for i in range(max(size-3, 0), size):
            context.append(
                {'role': 'user', 'content': st.session_state['user_input'][i]})
            context.append(
                {'role': 'assistant', 'content': st.session_state[context_data][i]})
    # 添加最新的用戶提示
    context.append({'role': 'user', 'content': str(prompt)})
    return context


# 生成自然語言
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
# Neo4j 數據庫結果
if 'database_results' not in st.session_state:
    st.session_state['database_results'] = []
# 用戶輸入
if 'user_input' not in st.session_state:
    st.session_state['user_input'] = []
# 生成的 Cypher 語句
if 'cypher' not in st.session_state:
    st.session_state['cypher'] = []


def get_text():
    input_text = st.text_input(
        "Ask away", "", key="input")
    return input_text


# 定義列
col1, col2 = st.columns([2, 1])

with col2:
    another_placeholder = st.empty()
with col1:
    placeholder = st.empty()
user_input = get_text()


if user_input:
    cypher = generate_cypher(generate_context(user_input, 'database_results'))
    # 如果不是有效的 Cypher 語句
    if not "MATCH" in cypher:
        print('No Cypher was returned')
        st.session_state.user_input.append(user_input)
        st.session_state.generated.append(
            cypher)
        st.session_state.cypher.append(
            "No Cypher statement was generated")
        st.session_state.database_results.append("")
    else:
        # 查詢數據庫，用戶ID是硬編碼的
        results = run_query(cypher, {'userId': USER_ID})
        # Harcode 結果限制為 10
        results = results[:10]
        # 圖2文本
        answer = generate_response(generate_context(
            f"Question was {user_input} and the response should include only information that is given here: {str(results)}"))
        st.session_state.database_results.append(str(results))
        st.session_state.user_input.append(user_input)
        st.session_state.generated.append(answer),
        st.session_state.cypher.append(cypher)


# 消息佔位符
with placeholder.container():
    if st.session_state['generated']:
        size = len(st.session_state['generated'])
        # 只顯示最後3次交換
        for i in range(max(size-3, 0), size):
            message(st.session_state['user_input'][i],
                    is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))


# 生成的 Cypher 語句
with another_placeholder.container():
    if st.session_state['cypher']:
        st.text_area("Latest generated Cypher statement",
                     st.session_state['cypher'][-1], height=240)
