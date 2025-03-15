# utils/database.py
import streamlit as st
import pandas as pd

def save_to_supabase(conn, table_name, df):
    data = df.to_dict(orient="records")
    try:
        conn.table(table_name).insert(data).execute()
        st.success(f"Dados salvos na tabela {table_name} com sucesso!")
    except Exception as e:
        st.error(f"Erro ao salvar no Supabase: {e}")

def load_from_supabase(conn, table_name):
    try:
        response = conn.table(table_name).select("*").execute()
        return pd.DataFrame(response.data)
    except Exception as e:
        st.error(f"Erro ao carregar do Supabase: {e}")
        return pd.DataFrame()
