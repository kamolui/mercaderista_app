import pandas as pd

def create_count_barplot(df):
    """
    Process a DataFrame to group records by classification and category, then reshape for plotting.

    The function performs the following steps:
    - Group the records by 'tipo_alerta' and 'categoria' and count the occurrences.
    - Rename the columns to 'tipo_alerta', 'categoria', and 'cantidad'.
    - Pivot the table to have 'categoria' as index and 'tipo_alerta' as columns.
    - Fill NaN values with 0.
    - Melt the DataFrame into a long format suitable for Plotly.

    Parameters:
    - df (pd.DataFrame): The source DataFrame with 'tipo_alerta' and 'categoria'.

    Returns:
    - pd.DataFrame: A DataFrame in long format with 'categoria', 'Status', and 'Casos'.
    """
    
    # Convert 'Fecha' to datetime
    df['Fecha'] = pd.to_datetime(df['Fecha'])

    # Group by 'clasificacion' and 'categoria', then get the index of the max 'Fecha' for each group
    idx = df.groupby(['tipo_alerta', 'categoria'])['Fecha'].idxmax()

    # Use the indices to filter the original DataFrame
    max_fecha_df = df.loc[idx].reset_index(drop=True)

    # If you need to count the occurrences again for some reason, you can apply your original grouping and size calculation here
    grouped = max_fecha_df.groupby(['tipo_alerta', 'categoria']).size().reset_index()

    # Rename the columns
    grouped.columns = ['tipo_alerta', 'categoria', 'cantidad']

    # Pivot and fill NaN values with 0
    grouped = grouped.pivot_table(index='categoria', columns='tipo_alerta', values='cantidad', aggfunc='sum').fillna(0).reset_index()

    # Convert the data to "long" format for Plotly
    long_data = grouped.melt(id_vars='categoria', var_name='Status', value_name='Casos').sort_values(by='Casos', ascending=True)

    return long_data

def create_sum_barplot(df):
    """
    Process a DataFrame to group records by classification and category, then reshape for plotting.

    The function performs the following steps:
    - Group the records by 'tipo_alerta' and 'categoria' and count the occurrences.
    - Rename the columns to 'tipo_alerta', 'categoria', and 'cantidad'.
    - Pivot the table to have 'categoria' as index and 'tipo_alerta' as columns.
    - Fill NaN values with 0.
    - Melt the DataFrame into a long format suitable for Plotly.

    Parameters:
    - df (pd.DataFrame): The source DataFrame with 'tipo_alerta' and 'categoria'.

    Returns:
    - pd.DataFrame: A DataFrame in long format with 'categoria', 'Status', and 'Casos'.
    """
    
    # Convert 'Fecha' to datetime
    df['Fecha'] = pd.to_datetime(df['Fecha'])

    # Group by 'clasificacion' and 'categoria', then get the index of the max 'Fecha' for each group
    idx = df.groupby(['tipo_alerta', 'categoria'])['Fecha'].idxmax()

    # Use the indices to filter the original DataFrame
    max_fecha_df = df.loc[idx].reset_index(drop=True)

    # If you need to count the occurrences again for some reason, you can apply your original grouping and size calculation here
    grouped = max_fecha_df.groupby(['tipo_alerta', 'categoria'])['oportunidad_valor'].sum().reset_index()

    # Rename the columns
    grouped.columns = ['tipo_alerta', 'categoria', 'cantidad']

    # Pivot and fill NaN values with 0
    grouped = grouped.pivot_table(index='categoria', columns='tipo_alerta', values='cantidad', aggfunc='sum').fillna(0).reset_index()

    # Convert the data to "long" format for Plotly
    long_data = grouped.melt(id_vars='categoria', var_name='Status', value_name='Casos').sort_values(by='Casos', ascending=True)

    return long_data