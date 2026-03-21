import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def get_secret(key: str):
    try:
        # Try Streamlit secrets (works on Streamlit Cloud)
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        # If st.secrets doesn't exist (e.g., on Render), skip safely
        pass

    # Fallback to environment variables (works on Render and locally)
    return os.getenv(key)