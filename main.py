import streamlit as st
import openai
import os
import json
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

with open('options.json', encoding='utf-8') as file:
  file_contents = file.read()
options_content = json.loads(file_contents)


if 'language' not in st.session_state:
    st.session_state['language'] = 'English'

langoption = st.sidebar.selectbox('Language/语言', ['English', '中文'], key='language')

# Update content based on language
if langoption == 'English':
    content = options_content["EN"]
else:
    content = options_content["CN"]


with st.form("my_form"):
    with st.sidebar:
        languageArr = ['English', '中文']

        st.session_state.update({
            'class_array': content['class'],
            'grade_array': content['grade'],
            'class_title': content['class_title'],
            'grade_title': content['grade_title'],
            'input_text': content['input_text'],
            'sub_text': content['sub_text'],
            'spinner_text': content['spinner_text']
        })

        classArr = st.session_state['class_array']
        classoption = st.selectbox(st.session_state['class_title'], classArr)

        gradeArr = st.session_state['grade_array']
        gradeoption = st.selectbox(st.session_state['grade_title'], gradeArr)

        question = st.text_input(st.session_state['input_text'])

        submitted = st.form_submit_button(st.session_state['sub_text'])

    if submitted and question:
        with st.spinner(st.session_state['spinner_text']):

            system_prompt = f"""你是一个专业的{gradeoption}{classoption}老师，你收到了学生提出的{question}问题，需要很专业的从理论背景，到推理过程，到最后结果的计算详尽的为学生解答数学问题，力争让每个人都能通过你的解答完全学会题目的解答原理。不仅仅是提供一个简单的计算结果或者答案。最后给出的答案，有语言的限制，请用{langoption}回答，请注意减少你对如何给他人教学的建议，只提供问题的详细解答就行。"""

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