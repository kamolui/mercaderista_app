import streamlit as st
from streamlit_extras.switch_page_button import switch_page

def create_page_switch_buttons(column_names_actions):
    """
    Creates a set of buttons in a Streamlit app that switch pages based on the button clicked.

    Args:
    - column_names_actions (list of tuples): A list where each tuple contains the button label 
      and the corresponding page name to switch to.
    """
    columns = st.columns(len(column_names_actions))  # Create columns based on the number of actions provided
    
    for col, (button_label, page_name) in zip(columns, column_names_actions):
        with col:
            if st.button(button_label):
                switch_page(page_name)
            else:
                pass