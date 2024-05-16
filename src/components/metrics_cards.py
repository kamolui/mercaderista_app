import streamlit as st

def create_metric_card(title, value, delta=None, delta_percentage=None):
    """
    Creates a metric card within a Streamlit container.

    The card displays a title and a primary metric value. Optionally, it can also show a delta value
    and a delta percentage to indicate the change from a previous value, formatted as "delta (delta_percentage%)".
    The delta and delta percentage are shown only if both are provided.

    Args:
    - title (str): The title of the metric card.
    - value (str): The primary metric value to display.
    - delta (str, optional): The delta value to show next to the primary metric, indicating the 
      change from a previous value. Default is None, meaning no delta is shown.
    - delta_percentage (str, optional): The percentage change of the delta value, shown in 
      parentheses next to the delta. Default is None.

    Returns:
    None: This function creates a Streamlit container with a metric card and does not return anything.
    """
    with st.container():
        st.subheader(title)
        if delta is not None and delta_percentage is not None:
            st.metric(label="", value=value, delta=f"{delta}\n{delta_percentage}", delta_color='off')
        else:
            st.metric(label="", value=value)
