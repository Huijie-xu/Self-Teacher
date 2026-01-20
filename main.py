import streamlit as st
import json
from src.OpenAICaller import OpenAICaller

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

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

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

# Chat input
question = st.chat_input(st.session_state['input_text'])

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if question:
    # Display user message
    with st.chat_message("user"):
        st.write(question)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": question})

    # Generate AI response
    with st.spinner(st.session_state['spinner_text']):
        system_prompt = f"""你是一个专业的{gradeoption}{classoption}老师，你收到了学生提出的{question}问题，需要很专业的从理论背景，到推理过程，到最后结果的计算详尽的为学生解答数学问题，力争让每个人都能通过你的解答完全学会题目的解答原理。不仅仅是提供一个简单的计算结果或者答案。最后给出的答案，有语言的限制，请用{langoption}回答，请注意减少你对如何给他人教学的建议，只提供问题的详细解答就行。请注意，当你解答数学问题的时候，不要用LaTeX 数学符号！就简单的用*乘号*，/除号，^指数符号等来表示数学运算符号就行。"""

        messages = [{"role": "system", "content": system_prompt}]
        for msg in st.session_state.messages:
            messages.append({"role": msg["role"], "content": msg["content"]})
        messages.append({"role": "user", "content": question})

        openai_caller = OpenAICaller()
        assistant_response = openai_caller.chat_completion(messages)

        # Display assistant response
        with st.chat_message("assistant"):
            st.write(assistant_response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})