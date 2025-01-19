import streamlit as st
from openai import OpenAI
import sys

with st.sidebar:
    st.markdown(f"""
 <center>
<img src='http://tuchuang.jojo-shuang.top/temp/119046852_p0.png'width='100'/>
<h1> MoBot <sup>beta</sup><h1/>
</center>""",unsafe_allow_html=True)
    system_message=st.text_area("角色定义","你是一个能帮助用户的ai助手")
    temperature=st.slider("创造力调节",min_value=0.0,max_value=2.0,step=0.1)
st.title("🤖Ai聊天机器人")
# 初始化界面的聊天框
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": "HI I am MoBot 很高兴为您服务"
    }, {
        "role": "user",
        "content": "你好"
    }]

# 展示历史聊天记录
for message in st.session_state.messages:
    # 增加对 'content' 键存在性的检查
    if "content" in message:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    else:
        # 如果 'content' 不存在，可以适当处理，比如打印警告或跳过这条消息
        st.warning(f"Warning: Message missing 'content': {message}")

# 初始化OpenAI客户端
client = OpenAI(api_key="sk-be9be9b062f340d2b20bea38375e4173", base_url="https://api.deepseek.com")

# 初始化消息历史
if "messageHistory" not in st.session_state:
    st.session_state.messageHistory = []


def chat_stream(query, system_message = None, temperature = 1):
    if system_message:
        st.session_state.messageHistory.append({"role": "system", "content": system_message})
    st.session_state.messageHistory.append({"role": "user", "content": query})
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=st.session_state.messageHistory,
        stream=True
    )
    return response


# 用户输入
user_query = st.chat_input("说点什么...")
if user_query:
    with st.chat_message("user"):
        st.write(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("assistant"):
        with st.spinner(""):
            response = chat_stream(user_query, system_message, temperature)
            message_placeholder = st.empty()
            ai_response = ""
            for chunk in response:
                if chunk.choices and hasattr(chunk.choices[0].delta, "content"):
                    ai_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
