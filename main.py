import streamlit as st
from openai import AzureOpenAI
import os
from dotenv import load_dotenv

# gets the API Key from environment variable AZURE_OPENAI_API_KEY
client = AzureOpenAI(
    # https://learn.microsoft.com/en-us/azure/ai-services/openai/reference#rest-api-versioning
    api_version="1106-Preview",
    # https://learn.microsoft.com/en-us/azure/cognitive-services/openai/how-to/create-resource?pivots=web-portal#create-a-resource
    azure_endpoint="https://joyxugpt4.openai.azure.com/",
    api_key="56215d89c1d14bb39c10080a0316bc29",
)


st.set_page_config(
    page_title="私人老师",
    layout="centered",
)

with st.form("my_form"):
    question = st.text_input('请输入你的问题')

    submitted = st.form_submit_button("Submit")

    if submitted and question:
        with st.spinner('加载解读中，请稍等 ......'):

            system_prompt = """你是一个专业的小学数学老师，你收到了学生提出的数学问题，需要很专业的从理论背景，到推理过程，到最后结果的计算详尽的为学生解答数学问题，力争让每个人都能通过你的解答完全学会题目的解答原理。不仅仅是提供一个简单的计算结果或者答案。"""

            completion = client.chat.completions.create(
                model="gpt4",
                messages = [{"role":"system","content":system_prompt},
                        {"role":"user","content":f"""
                        我遇到问题是:{question}"""},
                        ])

        with st.chat_message("assistant"):
            st.write(completion.choices[0].message.content)