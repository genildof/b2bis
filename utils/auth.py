# utils/auth.py
import streamlit as st

def login(conn, email, password):
    try:
        response = conn.auth.sign_in_with_password({"email": email, "password": password})
        st.write("Resposta completa do Supabase:", response)  # Debug completo
        if hasattr(response, "user"):
            st.write("Dados do usuário:", response.user)  # Mostra o objeto user
            return response.user
        else:
            st.error("Nenhum usuário encontrado na resposta.")
            return None
    except Exception as e:
        st.error(f"Erro ao fazer login: {e}")
        return None

def logout():
    st.session_state["logged_in"] = False
    st.session_state.pop("user", None)
