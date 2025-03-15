# pages/data_grid.py
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from utils.database import save_to_supabase

st.title("Grade de Edição de Dados")

conn = st.connection("supabase", type=SupabaseConnection)

if "correlation_result" in st.session_state:
    df = st.session_state["correlation_result"]
    
    # Configuração da grade
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_grid_options(enableRangeSelection=True, editable=True)
    grid_options = gb.build()

    # Exibição da grade
    grid_response = AgGrid(
        df,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        fit_columns_on_grid_load=True
    )
    
    edited_df = grid_response["data"]
    if st.button("Salvar Alterações"):
        save_to_supabase(conn, "correlation_result", edited_df)
        st.session_state["correlation_result"] = edited_df
        st.success("Alterações salvas no Supabase!")
else:
    st.error("Execute a correlação primeiro.")
