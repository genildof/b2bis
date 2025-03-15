# pages/upload_base_rede.py
import streamlit as st
import pandas as pd
from utils.database import save_to_supabase

st.title("Upload - Base Rede")

conn = st.connection("supabase", type=SupabaseConnection)

# Solicitação das abas e colunas
st.write("Por favor, me diga quais abas e colunas importar da Base Rede.")
sheet_name = st.text_input("Nome da aba do Excel (ex: 'Sheet1')", value="ANALITICO")
columns = st.text_input("Colunas a importar (separadas por vírgula, ex: 'A,B,C')", value="wcd,ATP/OSX,PEDIDO,DATA ENTRADA PROJETO,STATUS_4Field,CONTRATADA,Prazo Rede")

uploaded_file = st.file_uploader("Carregue a Base Rede (Excel)", type=["xlsx"])
if uploaded_file:
    with st.spinner("Processando..."):
        df = pd.read_excel(uploaded_file, sheet_name=sheet_name, usecols=columns.split(",") if columns else None)
        st.write("Prévia dos dados:")
        st.dataframe(df.head())
        if st.button("Salvar e Continuar"):
            save_to_supabase(conn, "base_rede", df)
            st.session_state["base_rede"] = df
            st.success("Dados salvos! Vá para a próxima página.")
