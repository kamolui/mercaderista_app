import pandas as pd

def transform_data(df):
    """
    Transforms a DataFrame with 'clasificacion', 'DDI', and 'tienda_dsc' columns 
    into a summarized format similar to the provided image. It creates a summary 
    for 'Casos Preagotados' and 'Casos Excedentes', takes the mean of the 'DDI' 
    and 'Inventario_Unidades', and appends a total row at the end.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame to transform.

    Returns:
    pd.DataFrame: The transformed DataFrame with aggregated values and a total row.
    """
    
    # Map 'clasificacion' to new columns for counting.
    df['Casos Preagotados'] = df['clasificacion'].apply(lambda x: 1 if x == 'Preagotado' else 0)
    df['Casos Excedentes'] = df['clasificacion'].apply(lambda x: 1 if x == 'Excedente' else 0)

    # Convert 'Fecha' to datetime
    df['Fecha'] = pd.to_datetime(df['Fecha'])

    # Group by 'clasificacion' and 'categoria', then get the index of the max 'Fecha' for each group
    idx = df.groupby(['tienda_dsc', 'categoria'])['Fecha'].idxmax()

    # Use the indices to filter the original DataFrame
    max_fecha_df = df.loc[idx].reset_index(drop=True)

    # Group by 'tienda_dsc' and aggregate the counts and averages.
    result = max_fecha_df.groupby(['tienda_dsc', 'categoria']).agg({
        'Casos Preagotados': 'sum',
        'Casos Excedentes': 'sum',
        'Inventario_Unidades': 'mean',
        'DDI': 'mean',
        'oportunidad_valor': 'sum'
    }).reset_index().fillna(0)

    # Rename columns to match the image.
    result.columns = ['Tienda', 'Categoria', 'Casos Preagotados', 'Casos Excedentes', 'Inventario', 'DDI', 'Oportunidad']

    # Calculate sum for 'Casos Preagotados' and 'Casos Excedentes'.
    totals = result[['Casos Preagotados', 'Casos Excedentes']].sum().to_dict()

    # Calculate mean for 'DDI' and 'Inventario'.
    totals['DDI'] = result['DDI'].mean()
    totals['Inventario'] = result['Inventario'].mean()
    totals['Oportunidad'] = result['Oportunidad'].sum()
    totals['Tienda'] = 'Total'
    totals['Categoria'] = ' '

    # Create the total row and format it correctly.
    total_df = pd.DataFrame([totals], columns=result.columns)
    total_df['DDI'] = total_df['DDI'].astype(int)
    total_df['Inventario'] = total_df['Inventario'].round(2)

    # Append the total row to the result DataFrame.
    result = pd.concat([result, total_df], ignore_index=True)

    # Format the result DataFrame 'DDI' and 'Inventario' as needed.
    result['DDI'] = result['DDI'].astype(int)
    result['Inventario'] = result['Inventario'].round(2)
    
    result.sort_values('Oportunidad')

    return result

# Example usage:
# df = pd.read_csv('path_to_your_csv.csv')
# transformed_df = transform_data(df)
# print(transformed_df)
