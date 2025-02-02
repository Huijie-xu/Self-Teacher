import streamlit as st
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# gets the API Key from environment variable AZURE_OPENAI_API_KEY
openai.api_type = os.getenv("OPENAI_API_TYPE")
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_version = os.getenv("OPENAI_API_VERSION")
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(
    page_title="私人老师",
    layout="centered",
)

with st.form("my_form"):
    with st.sidebar:
        languageArr = ['English', '中文']
        langoption = st.selectbox('Language', languageArr)

        classArr = ['数学','语文','英语']
        classoption = st.selectbox('科目', classArr)

        gradeArr = ['小学','初中','高中']
        gradeoption = st.selectbox('学级', gradeArr)

        question = st.text_input('请输入你的问题')

        submitted = st.form_submit_button("Submit")

    if submitted and question:
        with st.spinner('加载解读中，请稍等 ......'):

            system_prompt = f"""你是一个专业的{gradeoption}{classArr}老师，你收到了学生提出的{classArr}问题，需要很专业的从理论背景，到推理过程，到最后结果的计算详尽的为学生解答数学问题，力争让每个人都能通过你的解答完全学会题目的解答原理。不仅仅是提供一个简单的计算结果或者答案。最后给出的答案，有语言的限制，请用{langoption}回答"""

            response = openai.ChatCompletion.create(
                engine="gpt4",
                messages = [{"role":"system","content":system_prompt},
                        {"role":"user","content":f"""
                        我遇到问题是:{question}"""},
                        ],
                        temperature=0.7,
                        top_p=0.95,
                        frequency_penalty=0.5,
                        presence_penalty=0.1,
                        stop=None)

        with st.chat_message("assistant"):
            st.write(response.choices[0].message.content)