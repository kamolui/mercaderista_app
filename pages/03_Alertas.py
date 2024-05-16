import streamlit as st
import pandas as pd
import plotly.express as px

import config
from src.components.select_pages_buttons import create_page_switch_buttons
from src.components.metrics_cards import create_metric_card
from src.components.alerts_bar_plots import create_count_barplot, create_sum_barplot

st.header('Selecciona un reporte para revisar')
    
# Buttons to change page
with st.container(border=True):
   create_page_switch_buttons(config.column_names_actions)

data_alert = pd.read_csv(r'data\alertas_mercaderistas.csv')

# Layout with columnss
col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])

# Container of the metrics
with st.container(border=True):
    
    # Column 1: Metric card for "Cantidad de Alertas" 
    with col1:
        count_oportunidad_valor = data_alert.shape[0] 
        sum_oportunidad_valor = data_alert.oportunidad_valor.sum()
        
        create_metric_card("Cantidad de Alertas", 
                           f'{count_oportunidad_valor:.2f}', 
                           "Opor", 
                           f" ${sum_oportunidad_valor:.2f}"
        )

    # Column 2: Metric card for "Ajuste de inventario"
    with col2: 
        count_aj_inv = data_alert[data_alert['tipo_alerta'] == 'Ajuste de inventario'].shape[0]
        pct_aj_inv = count_aj_inv / count_oportunidad_valor * 100
        sum_aj_inv = data_alert[data_alert['tipo_alerta'] == 'Ajuste de inventario'].oportunidad_valor.sum()
        
        create_metric_card("Ajuste de Inventario", 
                           f"{count_aj_inv:.2f}", 
                           f"{pct_aj_inv:.2f}%", 
                           f"Opor ${sum_aj_inv:.2f}"
        )

    # Column 3: Metric card for "Inventario agotado"
    with col3:
        count_no_inv = data_alert[data_alert['tipo_alerta'] == 'Inventario agotado'].shape[0]
        pct_no_inv = count_no_inv / count_oportunidad_valor * 100
        sum_no_inv = data_alert[data_alert['tipo_alerta'] == 'Inventario agotado'].oportunidad_valor.sum()
        
        create_metric_card("Inventario agotado", 
                           f"{count_no_inv:.2f}", 
                           f"{pct_no_inv:.0f}%", 
                           f"Opor ${sum_no_inv:.2f}"
        )

    # Column 4: Metric card for "Inventario sin venta"
    with col4:
        count_no_sales = data_alert[data_alert['tipo_alerta'] == 'Inventario sin venta'].shape[0]
        pct_no_sales = count_no_sales / count_oportunidad_valor * 100
        sum_no_sales = data_alert[data_alert['tipo_alerta'] == 'Inventario sin venta'].oportunidad_valor.sum()
        
        create_metric_card("Inventario sin Venta", 
                           f"{count_no_sales:.2f}", 
                           f"{pct_no_sales:.0f}%", 
                           f"Opor ${sum_no_sales:.2f}"
        )
        
    # Column 5: Metric card for "Inventario baja Rotacion"
    with col5:
        count_low_rot = data_alert[data_alert['tipo_alerta'] == 'Baja rotacion'].shape[0]
        pct_low_rot = count_no_sales / count_oportunidad_valor * 100
        sum_low_rot = data_alert[data_alert['tipo_alerta'] == 'Baja rotacion'].oportunidad_valor.sum()
        
        create_metric_card("Inventario con Baja Rotacion", 
                           f"{count_low_rot:.2f}", 
                           f"{pct_low_rot:.0f}%", 
                           f"Opor ${sum_low_rot:.2f}"
        )
        
# Line plot sales vs inv vs inv moving
line_data = data_alert.groupby('Fecha')[['oportunidad_valor','inventario_unidades']].sum().sort_values('Fecha').reset_index()

fig = px.line(line_data, x='Fecha', y='oportunidad_valor', markers=True, title='Ventas e Inventario por tiempo', labels={'Ventas_Unidades': 'Ventas'})
fig.add_scatter(x=line_data['Fecha'], y=line_data['inventario_unidades'], name='Inventario Tienda')

st.plotly_chart(fig, use_container_width=True)

# Bar plot for count and sum
count_bar_col, sum_bar_col = st.columns([2, 2])

# Convert the data to "long" format for Plotly
long_data_count = create_count_barplot(data_alert)

long_data_sum = create_sum_barplot(data_alert)

with count_bar_col:
    with st.container(height=470):
        # Create the bar chart
        # Plotting with Plotly
        fig = px.bar(
            long_data_count,
            y='categoria',
            x='Casos',
            color='Status',
            title='Casos por Categoria y Status',
            category_orders={"Status": ["Inventario agotado", "Inventario sin venta", "Ajuste de inventario"]}  # Ensure correct order
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
        
with sum_bar_col:
    with st.container(height=470):
        # Create the bar chart
        # Plotting with Plotly
        fig = px.bar(
            long_data_sum,
            y='categoria',
            x='Casos',
            color='Status',
            title='Casos por Categoria y Status',
            category_orders={"Status": ["Inventario agotado", "Inventario sin venta", "Ajuste de inventario"]}  # Ensure correct order
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
        
# Actions Table
# Convert 'Fecha' to datetime
data_alert['Fecha'] = pd.to_datetime(data_alert['Fecha'])

# Group by 'clasificacion' and 'categoria', then get the index of the max 'Fecha' for each group
idx = data_alert.groupby(['tienda_dsc', 'descripcion_producto', 'tipo_alerta'])['Fecha'].idxmax()

# Use the indices to filter the original DataFrame
max_fecha_df = data_alert.loc[idx].reset_index(drop=True)

data = (max_fecha_df
        .groupby(['tienda_dsc', 'descripcion_producto', 'tipo_alerta'])
        .agg({'oportunidad_valor': 'sum'})
        .reset_index()
        .fillna(0)
        .sort_values(['tienda_dsc', 'oportunidad_valor'], ascending=False))

totals = data[['oportunidad_valor']].sum().to_dict()
totals['tienda_dsc'] = 'Total'
totals['descripcion_producto'] = ' '
totals['tipo_alerta'] = ' '

# Create the total row and format it correctly.
total_df = pd.DataFrame([totals], columns=data.columns)

# Append the total row to the result DataFrame.
result = pd.concat([data, total_df], ignore_index=True)   

result.columns = ['Tienda',	'Producto',	'Alerta', 'Oportunidad']

with st.container(height=470, border=True):        
    st.table(result) 