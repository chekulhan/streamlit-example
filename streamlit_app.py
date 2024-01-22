import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
from openai import OpenAI

from time import sleep
"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:.
If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""



st.session_state.go = False


if 'go' not in st.session_state:
    st.session_state.go = False

def click_action():
    st.session_state.go = True

st.write(st.session_state.go)

pregunta = st.text_input('Introducir tu pregunta...', value ='¿Cómo se llama el proyecto?')

st.button('Go', on_click=click_action())


if st.session_state.go == True:
    
    client = OpenAI(api_key=st.secrets["API_KEY"])
    
    ASSISTANT_ID = st.secrets["ASSISTANT_ID"]

    assistant = client.beta.assistants.retrieve(ASSISTANT_ID)

    thread = client.beta.threads.create()

    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=pregunta,
    )


    run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
    )

    while (run.status != "completed") and (run.last_error != "None"):
        st.write(f"Esperando respuesta... {run.status}")
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        sleep(8)


    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    result = ",".join(str(e) for e in messages)
    result = st.text_area(result)
    
    st.write("end")

else:
    st.write("Esperando pregunta...")
