# app.py
import streamlit as st
from utils.auth import login, logout
from st_supabase_connection import SupabaseConnection
import logging

# Configuração de logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Configuração da página
st.set_page_config(page_title="Meu App", layout="wide")

# Tentativa de conexão com Supabase
st.write("Tentando carregar credenciais...")
try:
    secrets = st.secrets["connections"]["supabase"]
    st.write("Credenciais encontradas no secrets.toml:", list(secrets.keys()))
    url = secrets["SUPABASE_URL"]
    key = secrets["SUPABASE_KEY"]
    st.write("SUPABASE_URL:", url)
    st.write("SUPABASE_KEY (parcial):", key[:10] + "..." + key[-10:])  
    conn = st.connection("supabase", type=SupabaseConnection)
    st.write("Conexão com Supabase estabelecida com sucesso!")
    logger.info("Conexão com Supabase OK")
except Exception as e:
    st.error(f"Erro ao conectar ao Supabase: {e}")
    logger.error(f"Erro na conexão: {e}")
    st.stop()

# Estado da sessão para autenticação
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

def main():
    if not st.session_state["logged_in"]:
        st.title("Login")
        email = st.text_input("Email")
        password = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            st.write("Tentando autenticar...")
            user = login(conn, email, password)
            if user:
                st.session_state["logged_in"] = True
                st.session_state["user"] = user
                st.success("Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("Credenciais inválidas ou usuário não encontrado.")
    else:
        user = st.session_state["user"]
        # Tenta acessar o email de forma segura
        try:
            user_email = user.email if hasattr(user, "email") else "Usuário sem email"
            st.sidebar.title(f"Bem-vindo, {user_email}")
        except Exception as e:
            st.sidebar.title("Bem-vindo, Usuário")
            st.sidebar.warning(f"Erro ao acessar email: {e}")
        
        if st.sidebar.button("Sair"):
            logout()
            st.session_state["logged_in"] = False
            st.rerun()

        st.title("Home")
        st.write("Este é o seu painel principal. Navegue pelas opções no menu lateral.")
        st.sidebar.success("Selecione uma página acima")

if __name__ == "__main__":
    main()
