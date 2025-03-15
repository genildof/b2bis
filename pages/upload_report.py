# pages/upload_report.py
import streamlit as st
import pandas as pd
from utils.database import save_to_supabase

st.title("Upload - Report B2B")

conn = st.connection("supabase", type=SupabaseConnection)

# Solicitação das abas e colunas
st.write("Por favor, me diga quais abas e colunas importar do Report B2B.")
sheet_name = st.text_input("Nome da aba do Excel (ex: 'Sheet1')", value="Export")
columns = st.text_input("Colunas a importar (separadas por vírgula, ex: 'A,B,C')", value="Pedido,Dias_CarteiraAtual,TM_Tec_Total,Num_WCD,Num_ATP,Classificacao_Resumo_Atual,Quebra_Esteira,Esteira,Esteira_Regionalizada,Segmento_V3,Carteira,Cliente,Cidade,OSX,Cadeia_Pendencias_Descricao,DataTecnica,Produto,Servico,Delta_REC_LIQ,Tecnologia_Report,Aging_Resumo,Projetos,Projetos_Lote,Motivo_PTA_Cod,Origem_Pend,SLA_TECNICA")

uploaded_file = st.file_uploader("Carregue o Report B2B (Excel)", type=["xlsx"])
if uploaded_file:
    with st.spinner("Processando..."):
        df = pd.read_excel(uploaded_file, sheet_name=sheet_name, usecols=columns.split(",") if columns else None)
        st.write("Prévia dos dados:")
        st.dataframe(df.head())
        if st.button("Salvar e Continuar"):
            save_to_supabase(conn, "report_b2b", df)
            st.session_state["report_b2b"] = df
            st.success("Dados salvos! Vá para a próxima página.")
