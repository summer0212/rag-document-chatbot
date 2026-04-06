import streamlit as st


def initialize_params():
    if "messages" not in st.session_state:
        st.session_state.messages=[]

#why are we checking vector-store in session-state
    if 'vector_store' not in st.session_state:
        st.session_state.vector_store = None

    