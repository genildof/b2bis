# utils/auth.py
import streamlit as st

def login(conn, email, password):
    try:
        response = conn.auth.sign_in_with_password({"email": email, "password": password})
        user = response.user
        # Verifica se é admin no user_metadata
        is_admin = user.user_metadata.get("is_admin", False) if hasattr(user, "user_metadata") else False
        return {"user": user, "is_admin": is_admin}
    except Exception as e:
        st.error(f"Erro ao fazer login: {e}")
        return None

def logout():
    st.session_state["logged_in"] = False
    st.session_state.pop("user_data", None)
