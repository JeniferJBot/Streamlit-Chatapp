import streamlit as st
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory


@st.cache_resource
def build_chain(model: str, temperature: float):
    if any(item is None for item in [model, temperature]):
        st.error('Invalid Parameters')
    
    chat_template = ChatPromptTemplate.from_messages([
        ("system", "Your task is to answer the user's queries as accurately as possible."),
        ("placeholder", "{chat_history}"),
        ("user", "{input}")
    ])
    
    # ✅ FIXED: Using OpenAI instead of Ollama
    llm = ChatOpenAI(
        model=model,
        temperature=temperature
    )
    
    memory_chain = RunnableWithMessageHistory(
        chat_template | llm | StrOutputParser(),
        lambda x: StreamlitChatMessageHistory('langchain_messages')
    )
    
    return memory_chain
    

def get_response():
    chain = build_chain(
        model=st.session_state.get('MODEL', 'gpt-3.5-turbo'),
        temperature=st.session_state.get('TEMPERATURE', 0.7)
    )
    
    response = chain.stream(
        {'input': st.session_state.get('user_input')},
        config={'configurable': {'session_id': st.session_state.get('session_id')}}
    )
    
    st.session_state['response'] = response


def clear_chat_history():
    if st.session_state.get('clear'):
        st.session_state['langchain_messages'] = list()
