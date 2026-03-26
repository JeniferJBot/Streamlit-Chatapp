import secrets
import streamlit as st
import actions

# Assign a Session ID
if "session_id" not in st.session_state:
    st.session_state["session_id"] = secrets.token_hex(8)

# ----- SIDE BAR -----
with st.sidebar:
    
    st.title("AI Chatbot 🤖")
    st.markdown("Chat with OpenAI-powered assistant")

    model = st.selectbox(
        "Model",
        options=["gpt-3.5-turbo", "gpt-4o-mini"],
        key="MODEL"
    )
    
    temperature = st.slider(
        label='Temperature',
        key='TEMPERATURE',
        min_value=0.0,
        max_value=1.0,
        step=0.1,
        value=0.7
    )

    # ❌ Removed Connect button (not needed)

    st.button(
        label='Clear Chat',
        key='clear',
        on_click=actions.clear_chat_history,
        use_container_width=True
    )

# ----- MAIN PAGE -----

st.title('💬 Chatbot')
st.markdown(f"Model: `{st.session_state.get('MODEL')}`")

# Show chat history
if st.session_state.get('langchain_messages'):
    for idx, message in enumerate(st.session_state.get('langchain_messages'), start=1):
        role = 'human' if idx % 2 else 'assistant'
        with st.chat_message(role):
            st.write(message.content)

# Input box
user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state['user_input'] = user_input
    
    with st.chat_message('human'):
        st.write(user_input)
    
    actions.get_response()

# Show response
response = st.session_state.get('response')
if response:
    with st.chat_message('assistant'):
        st.write_stream(response)
    st.session_state['response'] = None
