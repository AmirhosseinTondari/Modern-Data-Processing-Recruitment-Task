import requests
import streamlit as st
import utils

# Page Config
st.set_page_config("Reasoning Implementation")

if "column_shape" not in st.session_state:
    st.session_state.column_shape = (0.82, 0.18)

st.markdown(
    """
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Rubik:wght@400;700&display=swap">
<style>
p, input, textarea, label, ul, li, ol, h1, h2, h3, h4, h5, h6 {
    font-family: 'Rubik', sans-serif;
}

.thoughts {
            color: gray; 
            font-style: italic;
            opacity: 0.7;
        }
</style>
""",
    unsafe_allow_html=True,
)

# Getting Messages
st.session_state.HISTORY = requests.request("get", url="http://127.0.0.1:8000/chat/history/").json()["messages"]

# Update Chat History
for message in st.session_state.HISTORY:
    if message["type"] == "human":
        with st.chat_message("user"):
            st.markdown(message["content"])
    else:
        with st.chat_message("ai"):
            st.markdown(message["content"])


sidebar = st.sidebar
# st.session_state.MEMORY = sidebar.checkbox("Memory", True)
# sidebar.markdown("___")
st.session_state.METHOD = sidebar.radio("Reasoning Method:", ["CoT", "CoT-sc", "ToT"])

chat_input = st.chat_input("پیام خود را اینجا تایپ کنید ...")

# Prompting model
if chat_input not in (None, "", " "):
    with st.chat_message("user"):
        st.markdown(chat_input)

    response_gen = utils.stream_response(f"http://127.0.0.1:8000/chat/{st.session_state.METHOD.lower()}/?message={chat_input}")
    with st.chat_message('ai'):
        response_container = st.empty()
        thoughts = ""
        final_response = ""
        for token in response_gen:
            if thoughts[-16:] != "Final Response: ":
                thoughts += token
            else:
                final_response += token
            
            formatted_thoughts = "".join(f'<p class="thoughts">{para}</p>' for para in thoughts.split("\n\n"))
            formatted_final_response = f'<p>{final_response}</p>'
            response_container.markdown(f'{formatted_thoughts} {formatted_final_response}', unsafe_allow_html=True)
