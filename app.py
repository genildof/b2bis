# app.py
import streamlit as st
from utils.auth import login, logout
from st_supabase_connection import SupabaseConnection

# Configuração da página
st.set_page_config(page_title="Meu App", layout="wide")

# Conexão com Supabase
conn = st.connection("supabase", type=SupabaseConnection)

# Estado da sessão para autenticação
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

def main():
    if not st.session_state["logged_in"]:
        st.title("Login")
        email = st.text_input("Email")
        password = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            user_data = login(conn, email, password)
            if user_data:
                st.session_state["logged_in"] = True
                st.session_state["user_data"] = user_data
                st.success("Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("Credenciais inválidas ou usuário não encontrado.")
    else:
        user_data = st.session_state["user_data"]
        user = user_data["user"]
        is_admin = user_data["is_admin"]
        
        # Sidebar com nome do usuário
        user_email = user.email if hasattr(user, "email") else "Usuário"
        st.sidebar.title(f"Bem-vindo, {user_email}")
        if st.sidebar.button("Sair"):
            logout()
            st.session_state["logged_in"] = False
            st.rerun()

        # Menu de navegação
        st.title("Home")
        st.write("Este é o seu painel principal. Navegue pelas opções no menu lateral.")
        
        # Páginas disponíveis para todos
        st.sidebar.success("Selecione uma página acima")
        page_options = ["upload report", "upload base rede"]
        
        # Páginas restritas a admins
        if is_admin:
            page_options.extend(["correlation", "data grid"])
            st.sidebar.write("Admin: Acesso total liberado.")
        else:
            st.sidebar.write("Acesso limitado (não-admin).")

        page = st.sidebar.selectbox("Escolha uma página", page_options)

        # Navegação
        if page == "upload report":
            st.write("Carregar página upload_report.py aqui.")
            # Adicione importação dinâmica ou chame a função da página
        elif page == "upload base rede":
            st.write("Carregar página upload_base_rede.py aqui.")
        elif page == "correlation" and is_admin:
            st.write("Carregar página correlation.py aqui.")
        elif page == "data grid" and is_admin:
            st.write("Carregar página data_grid.py aqui.")

if __name__ == "__main__":
    main()
