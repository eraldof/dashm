import pandas as pd
import altair as alt
import streamlit as st


st.set_page_config(page_title= "DashMulti", page_icon=":shark:", layout="wide")

data = pd.read_csv('galva.csv', sep=";", decimal=",")
data['DTMOV'] = pd.to_datetime(data['DTMOV'], dayfirst=True)
data['MES_ANO'] = data['DTMOV'].dt.to_period('M').astype(str)
resultado = data.groupby('MES_ANO')['QT'].sum().reset_index()


line_chart = alt.Chart(resultado).mark_line(point=True).encode(
    x=alt.X('MES_ANO', title='Meses', axis=alt.Axis(labelAngle=0)), 
    y=alt.Y('QT', title='Quantidade Vendida', scale=alt.Scale(domain=[0, max(resultado['QT']) * 1.3])),  
    tooltip=['MES_ANO', 'QT']  
).properties(
    title='Evolução Mensal de Vendas'  
)


st.title('Análise de Vendas Produtos Galvano')
st.altair_chart(line_chart, use_container_width=True)
