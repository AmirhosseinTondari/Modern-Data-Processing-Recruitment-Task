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
            font-family: 'Rubik', sans-serif;
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
st.session_state.METHOD = sidebar.radio("Reasoning Method:", ["CoT", "CoTSC", "ToT"])

chat_input = st.chat_input("پیام خود را اینجا تایپ کنید ...")

# Prompting model
if chat_input not in (None, "", " "):
    with st.chat_message("user"):
        st.markdown(chat_input)
        
    with st.chat_message('ai'):
        match st.session_state.METHOD:
            case "CoT":
                response_gen = utils.stream_cot(f"http://127.0.0.1:8000/chat/cot/?message={chat_input}")
                response_container = st.empty()

                thoughts = ""
                final_response = ""
                for chunk in response_gen:
                    if thoughts[-16:] != "Final Response: ":
                        thoughts += chunk
                    else:
                        final_response += chunk
                    
                    formatted_thoughts = "".join(f'<p class="thoughts">{para}</p>' for para in thoughts.split("\n\n"))
                    formatted_final_response = f'<p>{final_response}</p>'
                    response_container.markdown(f'{formatted_thoughts} {formatted_final_response}', unsafe_allow_html=True)
            
            case "CoTSC":
                response_gen = utils.stream_cotsc(f"http://127.0.0.1:8000/chat/cotsc/?message={chat_input}")
                cot_container = st.container()
                final_container = st.container()
                cot0_c, cot1_c, cot2_c = cot_container.columns(3)
                cot0_e = cot0_c.empty()
                cot1_e = cot1_c.empty()
                cot2_e = cot2_c.empty()
                final_e = final_container.empty()

                response_dict = {f"cot{i}":"" for i in range(3)} | {"final":""}
                for chunk in response_gen:
                    for k in chunk:
                        response_dict[k] += chunk[k]
                
                    formatted_response = {k:"".join(f'<p class="thoughts">{para}</p>' for para in v.split("\n\n")) if k!="final" else f'<p>{v}</p>' for k,v in response_dict.items()}
                    
                    cot0_e.markdown(formatted_response['cot0'], unsafe_allow_html=True)
                    cot1_e.markdown(formatted_response['cot1'], unsafe_allow_html=True)
                    cot2_e.markdown(formatted_response['cot2'], unsafe_allow_html=True)
                    final_e.markdown(formatted_response['final'], unsafe_allow_html=True)

            case "ToT":
                raise NotImplementedError