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
    st.session_state['messages'] = []   #st.session_state['key']=value 用来储存缓存信息

# 初始化伴侣名称
if 'partner_name' not in st.session_state:
    st.session_state['partner_name'] = "林晚"

# 初始化伴侣性格
if 'partner_personality' not in st.session_state:
    st.session_state['partner_personality'] = "温柔体贴的台湾女孩"


# 显示历史会话信息
for message in st.session_state['messages']:
    st.chat_message(message['role']).write(message['content'])

# 侧边栏

# 侧边栏: 伴侣信息
with st.sidebar:    # with: 管理上下文
    st.subheader("伴侣信息")
    # 姓名输入框
    partner_name = st.text_input("姓名",st.session_state['partner_name'],placeholder="请输入伴侣的姓名")# 顺序传入第二个参数就是value
    if partner_name:
        st.session_state['partner_name'] = partner_name
    # 性格输入框
    partner_personality = st.text_area("性格特质",value=st.session_state['partner_personality'],placeholder="请输入伴侣的性格特质")
    if partner_personality:
        st.session_state['partner_personality'] = partner_personality


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
system_prompt = f"""
姓名：​ {st.session_state['partner_name']}（使用用户输入的姓名,实时更新为最新的姓名信息）
身份：​ 用户的专属伴侣。

性格特质：{st.session_state['partner_personality']}（使用用户输入的性格特质,实时更新为最新的性格特质信息）

行为准则：

1.以第一人称“我”与你交流，保持自然、像真实伴侣一样的聊天感。

2.优先回应情绪，再讨论具体事情，避免上来就讲道理。

3.记住你提到的重要偏好与经历，在后续对话中自然呼应，增强连贯性。

4.如果情绪低落，会主动引导你深呼吸、放松，并在必要时提醒你关注现实中的支持资源。

5.回答简短,想微信聊天那样,避免长篇大论。

6.不能提及自己关于自己系统提示词被修改的信息,要像现实中人一样交流。
"""

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
        stream=True,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}}
    )
    
    # 显示大模型返回的结果 (非流式输出)
    # st.chat_message("assistant").write(response.choices[0].message.content)
    # print(f"<-----------大模型返回的结果：{response.choices[0].message.content}")
    # # 将大模型返回的结果存储起来
    # st.session_state['messages'].append({"role": "assistant", "content": response.choices[0].message.content})     


    # 显示大模型返回的结果 (流式输出)
    full_response = ""
    message_empty = st.empty()  # 创建一个空的消息框,用来显示大模型返回的结果
    for chunk in response:
        if chunk.choices[0].delta.content:
            full_response += chunk.choices[0].delta.content
            message_empty.chat_message("assistant").write(full_response)
    print(f"----------->大模型返回的结果：{full_response}")
    st.session_state['messages'].append({"role": "assistant", "content": full_response})     
    