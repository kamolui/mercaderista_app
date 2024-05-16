import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(r'data\alertas_mercaderistas.csv')

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
long_data = grouped.melt(id_vars='categoria', var_name='Status', value_name='Casos').sort_values(by='Casos', ascending=False)

print(long_data)