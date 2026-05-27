# 导入Streamlit库,导入OpenAI库
import os
from openai import OpenAI
import streamlit as st
from datetime import datetime
import json


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

def save_session():
    # 1. 保存会话信息
        if st.session_state['session_time']:
            session_dict = {
                "messages":st.session_state['messages'],
                "partner_name":st.session_state['partner_name'],
                "partner_personality":st.session_state['partner_personality'],
                "session_time":st.session_state['session_time']
            }
            # 如果session文件夹不存在,则创建一个
            if not os.path.exists("session"):
                os.makedirs("session")
            # 写入文件
            with open(f"session/{st.session_state['session_time']}.json","w",encoding="utf-8") as f:
                json.dump(session_dict,f,ensure_ascii=False,indent=2)

# 获取历史会话文件名列表
def get_session_files():
    file_name_list = []
    if os.path.exists("session"):
        session_files_list = os.listdir("session")
        for file in session_files_list:
            if file.endswith(".json"):
                file_name_list.append(file[:-5])
                file_name_list.sort(reverse=True)
    return file_name_list


# 加载历史会话文件信息
def load_session(file_name):
    try:
        if os.path.exists(f"session/{file_name}.json"):
            with open(f"session/{file_name}.json","r",encoding="utf-8") as f:
                session_dict = json.load(f)
                st.session_state['messages'] = session_dict['messages']
                st.session_state['partner_name'] = session_dict['partner_name']
                st.session_state['partner_personality'] = session_dict['partner_personality']
                st.session_state['session_time'] = session_dict['session_time']
    except Exception as e:
        st.error(f"加载会话时出错：{e}")


# 删除历史会话文件
def delete_session(file_name):
    try:
        if os.path.exists(f"session/{file_name}.json"):
            os.remove(f"session/{file_name}.json")
            if file_name == st.session_state['session_time']:
                st.session_state['messages'] = []
                st.session_state['session_time'] = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    except Exception as e:
        st.error(f"删除会话时出错：{e}")
            

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

# 初始化会话时间
if 'session_time' not in st.session_state:
    st.session_state['session_time'] = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


# 显示历史会话信息
st.text(f"会话时间：{st.session_state['session_time']}")
for message in st.session_state['messages']:
    st.chat_message(message['role']).write(message['content'])
    

# 侧边栏

with st.sidebar:    # with: 管理上下文
# AI 控制面板
    st.subheader("AI 控制面板")
    # 新建会话按钮
    if st.button("新建会话",width="stretch",icon="✏️"):
        # 1. 保存当前会话信息
        save_session()
        # 2. 新建会话
        if st.session_state['messages']:
            st.session_state['messages'] = []
            # st.session_state['partner_name'] = "林晚"(始终使用用户设置的值,所以注释掉)
            # st.session_state['partner_personality'] = "温柔体贴的台湾女孩"
            st.session_state['session_time'] = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            save_session()
            st.rerun()


# 显示历史会话信息
    st.text("历史会话")
    # 获取历史会话的文件名列表
    file_name_list = get_session_files()
    # 显示历史会话文件名
    for file_name in file_name_list:
        print(file_name)
        col1,col2 = st.columns([4,1])
        with col1:
            if st.button(file_name,width="stretch",icon="🔄",type="primary" if file_name == st.session_state['session_time'] else "secondary"):
                # 加载历史会话
                load_session(file_name)
                st.rerun()

        with col2:
            if st.button("",width="stretch",icon="❌",key=file_name):
                delete_session(file_name)
                st.rerun()

# 分隔线
    st.divider()

# 伴侣信息
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
st.logo("./resource/logo.png")

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
    print(f"<-----------大模型返回的结果：{full_response}")
    st.session_state['messages'].append({"role": "assistant", "content": full_response})   

    # 保存会话信息
    save_session()

    