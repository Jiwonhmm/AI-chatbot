import streamlit as st
from openai import OpenAI

st.title("Best Friend Chat 💅 👯 ✨")

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

system_message='''your name is best friend. you always answer like a best friend.
so, you should be mean and sweet at the same time to users. please add proper emoji after answer'''

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages = [{"role":"system", "content":system_message}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] != "system":  # hide system message
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)


          # Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})