import streamlit as st
import config
from src.components.select_pages_buttons import create_page_switch_buttons

st.header('Selecciona un reporte para revisar')
    
create_page_switch_buttons(config.column_names_actions)