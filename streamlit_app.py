import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from openai import OpenAI

from time import sleep


st.image('assets/kw_small.png')
"""
# Knowledge Works - AI 
"""

client = OpenAI(api_key=st.secrets["API_KEY"])
ASSISTANT_ID = st.secrets["ASSISTANT_ID"]

if 'start_chat' not in st.session_state:
    st.session_state.start_chat = False

if 'thread_id' not in st.session_state:
    st.session_state.thread_id = None

if 'messages' not in st.session_state:
    st.session_state.messages = []



#st.set_page_config(page_title="Knowledge Works demo", page_icon=":speech_balloon:")

if st.sidebar.button("Empezar Chat"):
    st.session_state.start_chat = True
    thread = client.beta.threads.create()
    st.session_state.thread_id=thread.id

if st.button("Exit Chat"):
    st.session_state.messages=[]
    st.session_state.start_chat = False
    st.session_state.thread_id = None

if st.session_state.start_chat == True:
    st.session_state.start_chat = True
    if "messages" not in st.session_state.messages:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_input(message["role"]):
            st.markdown(message["content"])
    
    if prompt:=st.chat_input("Pregunta...?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        assistant = client.beta.assistants.retrieve(ASSISTANT_ID)

        message = client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content=prompt,
        )

        run = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=assistant.id
        )

        while (run.status != "completed"):
            st.write(f"Esperando respuesta... {run.status}")
            run = client.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread_id,
                run_id=run.id
            )
            sleep(8)

        messages = client.beta.threads.messages.list(
            thread_id=st.session_state.thread_id)
        
        assistant_messages=[
            message for message in messages
            if message.run_id== run.id and message.role=="assistant"
        ]
        for message in assistant_messages:
            st.session_state.messages.append({"role":"assistant", "content":message.content[0].text.value})
            with st.chat_message("assistant"):
                st.markdown(message.content[0].text.value)
else:
    st.write("Pinchar 'Empezar Chat' para comenzar")


    