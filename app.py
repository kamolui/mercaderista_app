import streamlit as st
from src.components.select_pages_buttons import create_page_switch_buttons
import config
from PIL import Image

# Home page
if __name__ == "__main__":  
      
    st.set_page_config(
        page_title="Mercaderista Dash",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    image = Image.open(r"assets\images\nestle_logo_header.png")
    new_image = image.resize((959, 275))
    st.columns(3)[1].image(new_image)
    
    st.title('App Mercaderista del Futuro')
    st.header('¡Hola! Selecciona un reporte para revisar')
    
    create_page_switch_buttons(config.column_names_actions)