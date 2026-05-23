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
    

    # 将提示词发送给大模型
    response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}, # 用户输入的问题
        ],
        stream=False,
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}}
    )
    # 显示大模型返回的结果
    st.chat_message("assistant").write(response.choices[0].message.content)
    print(f"<-----------大模型返回的结果：{response.choices[0].message.content}")
