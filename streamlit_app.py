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


client = OpenAI(api_key=st.secrets["API_KEY"])
ASSISTANT_ID = st.secrets["ASSISTANT_ID"]

assistant = client.beta.assistants.create(
    name="KW Educación Asistente",
    instructions="",
    tools=[{"type": "code_interpreter"}],

)

thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="¿Me puedes ayudar con información sobre la ley de educación?",
    
)


run = client.beta.threads.runs.create(
  thread_id=thread.id,
  assistant_id=ASSISTANT_ID
)

st.write(run)

while (run.status != "completed") or (run.failed_at == "None"):
    st.write(f"Working... {run.status}")
    st.write(run)
    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )
    sleep(8)

st.write(run)

messages = client.beta.threads.messages.list(
  thread_id=thread.id
)


st.write(messages)

num_points = st.slider("Number of points in spiral", 1, 10000, 1100)
num_turns = st.slider("Number of turns in spiral", 1, 300, 31)

indices = np.linspace(0, 1, num_points)
theta = 2 * np.pi * num_turns * indices
radius = indices

x = radius * np.cos(theta)
y = radius * np.sin(theta)

df = pd.DataFrame({
    "x": x,
    "y": y,
    "idx": indices,
    "rand": np.random.randn(num_points),
})

st.altair_chart(alt.Chart(df, height=700, width=700)
    .mark_point(filled=True)
    .encode(
        x=alt.X("x", axis=None),
        y=alt.Y("y", axis=None),
        color=alt.Color("idx", legend=None, scale=alt.Scale()),
        size=alt.Size("rand", legend=None, scale=alt.Scale(range=[1, 150])),
    ))
