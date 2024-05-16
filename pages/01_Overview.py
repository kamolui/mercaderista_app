import streamlit as st
import config
from src.components.select_pages_buttons import create_page_switch_buttons
from src.components.metrics_cards import create_metric_card
from src.components.overview_bar_plot import prepare_data_for_plot
from src.components.total_df import transform_data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go

# Page header
st.header('Overview')

# Buttons to change page
with st.container(border=True):
   create_page_switch_buttons(config.column_names_actions)

data_so = pd.read_csv(r'data\data_so.csv')
time_data = data_so.copy()

data_so['Fecha'] = pd.to_datetime(data_so['Fecha'])

# Find the latest date
latest_date = data_so['Fecha'].max() 

# Filter the records for the last date
data_so = data_so[data_so['Fecha'] == latest_date]

# Layout with columnss
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

# Container of the metrics
with st.container(border=True):
    # Column 1: Metric card for "Universo"
    with col1:
        count_data_so = data_so.shape[0] / 1_000_000
        count_preagotados = data_so[data_so['clasificacion'] == 'Preagotado'].shape[0] / 1_000_000
        list_excedentes = ['Excdente_1', 'Excdente_2', 'Excdente_3']
        count_excedentes = data_so[data_so.clasificacion.isin(list_excedentes)].shape[0] / 1_000_000
        
        create_metric_card("Universo", 
                           f'{count_data_so:.2f}m', 
                           f"Preagotado {count_preagotados:.2f}m", 
                           f"\nExcedente {count_excedentes:.2f}m"
        )

    # Column 2: Metric card for "Oportunidad"
    with col2:
        sum_oportunidad = data_so.oportunidad_valor.sum() / 1_000_000
        
        create_metric_card("Oportunidad", 
                           f"${sum_oportunidad:.2f}m", 
                           f"Casos {12}", 
                           f"Porcentaje de casos {1}%"
        )

    # Column 3: Metric card for "Oportunidad"
    with col3:
        mean_ddi = data_so.DDI.mean()
        
        create_metric_card("DDI", 
                           f'{mean_ddi:.2f}', 
                           ' ', 
                           ' '
        )

    # Column 4: Metric card for "Oportunidad"
    with col4:
        mean_sales_units = data_so.Ventas_Unidades.mean()
        mean_inv_units = data_so.Inventario_Unidades.mean()
        
        create_metric_card("Ventas",
                           f'{mean_sales_units:.2f}',
                           f'Inventario {mean_inv_units:.2f}',
                           ' '
        )


# Line plot DDi vs time
ddi_line_plot_data = time_data.groupby('Fecha')['DDI'].mean().reset_index()
fig = px.line(ddi_line_plot_data, x='Fecha', y='DDI', markers=True, title='DDI vs Tiempo')
st.plotly_chart(fig, use_container_width=True)


# Bar plot
bar_col, table_col = st.columns([2, 2])

# Convert the data to "long" format for Plotly
long_data = prepare_data_for_plot(data_so)

with bar_col:
    with st.container(height=470):
        # Create the bar chart
        # Plotting with Plotly
        fig = px.bar(
            long_data,
            y='categoria',
            x='Casos',
            color='Status',
            title='Casos por Categoria y Status',
            category_orders={"Status": ["Estable", "Preagotado", "Excedente_Total", "Excedente"]}  # Ensure correct order
        )

        # Update the layout to group the bars
        fig.update_layout(
            barmode='stack',
            title='Casos by Categoria and Status',
            xaxis_title='Categoria',
            yaxis_title='Casos',
            legend_title='Status',
        )

        # Show the plot in Streamlit
        st.plotly_chart(fig, use_container_width=True)
        
with table_col:
    with st.container(height=470):
        totals = transform_data(data_so)
        
        # Display the table in Streamlit
        st.table(totals)


# Line plot Sales & Inv vs time
line_data = time_data.groupby('Fecha')[['Ventas_Unidades','Inventario_Unidades','Inventario_Cedis']].sum().sort_values('Fecha').reset_index()

fig = px.line(line_data, x='Fecha', y='Ventas_Unidades', markers=True, title='Ventas e Inventario por tiempo', labels={'Ventas_Unidades': 'Ventas'})
fig.add_scatter(x=line_data['Fecha'], y=line_data['Inventario_Unidades'], name='Inventario Tienda')
fig.add_scatter(x=line_data['Fecha'], y=line_data['Inventario_Cedis'], name='Inventario Transito')

st.plotly_chart(fig, use_container_width=True)

# Tables
bar_col, table_col = st.columns([1,3])

with bar_col:
    with st.container(height=470):
        # Display the table in Streamlit
        st.table(totals.drop(['Categoria', 'Casos Preagotados', 'Casos Excedentes', 'Inventario'], axis=1))

with table_col:
    with st.container(height=470):
        
        # Convert 'Fecha' to datetime
        data_so['Fecha'] = pd.to_datetime(data_so['Fecha'])

        # Group by 'clasificacion' and 'categoria', then get the index of the max 'Fecha' for each group
        idx = data_so.groupby(['tienda_dsc', 'mg'])['Fecha'].idxmax()

        # Use the indices to filter the original DataFrame
        max_fecha_df = data_so.loc[idx].reset_index(drop=True)
        
        data = (max_fecha_df.groupby(['tienda_dsc', 'mg']).agg({
        'Inventario_Unidades': 'sum',
        'Ventas_Unidades': 'sum',
        'DDI': 'sum',
        'oportunidad_valor': 'sum'
    }).reset_index().fillna(0).sort_values(['tienda_dsc', 'oportunidad_valor'], ascending=False))

        totals = data[['Inventario_Unidades', 'Ventas_Unidades', 'DDI']].mean().to_dict()
        totals['oportunidad_valor'] = data['oportunidad_valor'].sum()
        totals['tienda_dsc'] = 'Total'
        totals['mg'] = ' '

        # Create the total row and format it correctly.
        total_df = pd.DataFrame([totals], columns=data.columns)

        # Append the total row to the result DataFrame.
        result = pd.concat([data, total_df], ignore_index=True)   
        
        st.table(result) 