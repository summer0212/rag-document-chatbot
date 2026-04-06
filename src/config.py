import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def get_api_key():
    '''Get GROQ API key from environment (.env) or Streamlit secrets (cloud).'''
    key = os.environ.get("GROQ_API_KEY")
    if key:
        return key
    
    try:
        return st.secrets["GROQ_API_KEY"]
    except (KeyError, FileNotFoundError):
        return None