# 导入Streamlit库,导入OpenAI库
import os
from openai import OpenAI
import streamlit as st


# 设置页面配置项
st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

# 标题
st.title("AI智能伴侣")

# Initialization: 初始化会话信息(创建一个能缓存会话信息的列表)
if 'messages' not in st.session_state:  #每进行一次会话都会重新执行文件,所以需要在每次会话开始时初始化一个空列表
    st.session_state['messages'] = []   #st.session_state用来储存缓存信息

# 显示历史会话信息
for message in st.session_state['messages']:
    st.chat_message(message['role']).write(message['content'])


# logo
st.logo("./rescource/logo.png")

# 创建客户对象
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com"
    )

# 用户输入框(提示词)
prompt = st.chat_input("请输入你的问题：")

# 系统提示词
system_prompt = "You are a helpful assistant"

# 显示消息框
if prompt:  # 避免提示词为空时,消息框显示None
    # 显示用户输入的问题
    st.chat_message("user").write(prompt)
    print(f"----------->调用AI大模型,提示词：{prompt}")
    st.session_state['messages'].append({"role": "user", "content": prompt})     # 将用户输入的问题存储起来

    # 将提示词发送给大模型
    # print(st.session_state['messages'])
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=[
            {"role": "system", "content": system_prompt},
            # {"role": "user", "content": prompt}, 用户输入的问题
            *st.session_state['messages'], # 历史会话信息(解包列表ls=[*ls1,*ls2,*ls3])
        ],
        stream=False,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}}
    )

    # 显示大模型返回的结果
    st.chat_message("assistant").write(response.choices[0].message.content)
    print(f"<-----------大模型返回的结果：{response.choices[0].message.content}")
    st.session_state['messages'].append({"role": "assistant", "content": response.choices[0].message.content})     # 将大模型返回的结果存储起来