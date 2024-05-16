import pandas as pd

def prepare_data_for_plot(data_so):
    """
    Process a DataFrame to group records by classification and category, then reshape for plotting.

    The function performs the following steps:
    - Group the records by 'clasificacion' and 'categoria' and count the occurrences.
    - Rename the columns to 'clasificacion', 'categoria', and 'cantidad'.
    - Pivot the table to have 'categoria' as index and 'clasificacion' as columns.
    - Fill NaN values with 0.
    - Sum the 'Excedente' columns into a single 'Excedente' column.
    - Drop individual 'Excedente' columns.
    - Sort the DataFrame based on the 'Excedente' column.
    - Melt the DataFrame into a long format suitable for Plotly.

    Parameters:
    - data_so (pd.DataFrame): The source DataFrame with 'clasificacion' and 'categoria'.

    Returns:
    - pd.DataFrame: A DataFrame in long format with 'categoria', 'Status', and 'Casos'.
    """
    
    # Convert 'Fecha' to datetime
    data_so['Fecha'] = pd.to_datetime(data_so['Fecha'])

    # Group by 'clasificacion' and 'categoria', then get the index of the max 'Fecha' for each group
    idx = data_so.groupby(['clasificacion', 'categoria'])['Fecha'].idxmax()

    # Use the indices to filter the original DataFrame
    max_fecha_df = data_so.loc[idx].reset_index(drop=True)

    # If you need to count the occurrences again for some reason, you can apply your original grouping and size calculation here
    grouped = max_fecha_df.groupby(['clasificacion', 'categoria']).size().reset_index()

    # Rename the columns
    grouped.columns = ['clasificacion', 'categoria', 'cantidad']

    # Pivot and fill NaN values with 0
    grouped = grouped.pivot_table(index='categoria', columns='clasificacion', values='cantidad', aggfunc='sum').fillna(0).reset_index()

    # Add a cumulative column for 'Excedente'
    grouped['Excedente'] = grouped[['Excedente_1', 'Excedente_2', 'Excedente_3']].sum(axis=1)

    # Drop the individual 'Excedente' columns and sort by 'Excedente'
    grouped_sorted = grouped.drop(['Excedente_1', 'Excedente_2', 'Excedente_3'], axis=1).sort_values(by='Excedente', ascending=True)

    # Convert the data to "long" format for Plotly
    long_data = grouped_sorted.melt(id_vars='categoria', var_name='Status', value_name='Casos')
    
    return long_data

# Example usage:
# final_df = prepare_data_for_plot(your_original_dataframe)
