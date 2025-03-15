# pages/correlation.py
import streamlit as st
from utils.correlation import run_correlation  # Importa a rotina

st.title("Correlação de Dados")

if "report_b2b" in st.session_state and "base_rede" in st.session_state:
    report = st.session_state["report_b2b"]
    base_rede = st.session_state["base_rede"]
    
    st.write("Dados carregados. Pronto para correlacionar.")
    if st.button("Executar Correlação"):
        with st.spinner("Executando correlação..."):
            # Por favor, me envie sua rotina de correlação
            result = run_correlation(report, base_rede)
            st.session_state["correlation_result"] = result
            st.write("Resultado da correlação:")
            st.dataframe(result)
            st.success("Correlação concluída! Vá para a grade de edição.")
else:
    st.error("Por favor, carregue os dados nas páginas anteriores.")
