# utils/auth.py
import streamlit as st

def login(conn, email, password):
    try:
        response = conn.auth.sign_in_with_password({"email": email, "password": password})
        return response.user
    except Exception as e:
        st.error(f"Erro ao fazer login: {e}")
        return None

def logout():
    st.session_state["logged_in"] = False
    st.session_state.pop("user", None)
