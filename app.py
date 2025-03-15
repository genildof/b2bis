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
    st.write("Credenciais encontradas no secrets.toml:", secrets.keys())
    conn = st.connection("supabase", type=SupabaseConnection)
    logger.info("Conexão com Supabase estabelecida com sucesso!")
except KeyError as ke:
    st.error(f"Erro: Credenciais não encontradas no secrets.toml - {ke}")
    st.write("Tentando fallback com credenciais manuais...")
    try:
        # Substitua pelos valores reais do seu Supabase
        conn = st.connection("supabase", type=SupabaseConnection, 
                             url="https://seu-projeto.supabase.co", 
                             key="sua-chave-api-aqui")
        st.write("Conexão via fallback bem-sucedida!")
    except Exception as e:
        st.error(f"Erro no fallback: {e}")
        st.stop()
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
            user = login(conn, email, password)
            if user:
                st.session_state["logged_in"] = True
                st.session_state["user"] = user
                st.success("Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("Credenciais inválidas")
    else:
        st.sidebar.title(f"Bem-vindo, {st.session_state['user']['email']}")
        if st.sidebar.button("Sair"):
            logout()
            st.session_state["logged_in"] = False
            st.rerun()

        st.title("Home")
        st.write("Este é o seu painel principal. Navegue pelas opções no menu lateral.")
        st.sidebar.success("Selecione uma página acima")

if __name__ == "__main__":
    main()
