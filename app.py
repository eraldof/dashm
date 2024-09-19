import pandas as pd
import numpy as np
import datetime as dt
import streamlit as st
import altair as alt


data = pd.read_csv("data.csv", sep = ";")
data['DATA'] = pd.to_datetime(data.loc[:,'DATA'], dayfirst=True)
data['FATURADO'] = data['FATURADO'].str.replace('.', '').str.replace(',', '.').astype(float)
data['CUSTO'] = data['CUSTO'].str.replace('.' , '').str.replace(',', '.').astype(float)
data = data.sort_values(by = 'DATA')

st.title("Dashboard Multipel :sunglasses:")



# Criando o gráfico de linha com pontos
line_chart = alt.Chart(data).mark_line(point=True).encode(
    x=alt.X('DATA:T', title='Dia', axis=alt.Axis(format='%d/%m')),  # Formatar datas para padrão brasileiro
    y=alt.Y('FATURADO', title='Faturamento (R$)', scale=alt.Scale(domain=[0, max(data['FATURADO']) * 1.3])),  # Ajustando eixo Y
    tooltip=['DATA:T', 'DIA', 'FATURADO']  # Tooltip para mostrar dados ao passar o cursor
).properties(
    title='Evolução Diária do Faturamento'
)

# Exibindo o gráfico no Streamlit
st.title('Análise do Faturamento')
st.altair_chart(line_chart, use_container_width=True)



tab1, tab2, tab3 = st.tabs(["Diário", "Semanal", "Mensal"])
with tab1:
    st.title("Métricas Diárias")

    
    d = st.date_input("Selecione uma data:",
                      format= 'DD/MM/YYYY',
                      min_value= dt.date(2024, 9, 1), max_value = dt.date(2024, 9, 30))
    
    t = data[data['DATA'] == str(d)]
    
    col1, col2, col3 = st.columns(3)

    with col1:
        try:
            st.metric(label="FATURAMENTO", value = str(t.iloc[0]['FATURADO']) + ' R$')
        except:
            st.metric(label="FATURAMENTO", value = '--')


    with col2: 
        margem = float(round(((t['FATURADO'] - t['CUSTO']) / t['FATURADO']) * 100, 2))

        st.metric(label="MARGEM", value = str(margem) + ' %')

    with col3:
        try:
            st.metric(label="MIX", value = t.iloc[0]['MIX'])
        except:
            st.metric(label="MIX", value = '--')


### FATURAMENTO POR DIA DA SEMANA
st.title('Análise do Faturamento por Dia da Semana')

faturamento_dia = data.groupby('DIA')['FATURADO'].sum().reset_index()
def clean(x):
    return x.strip()

faturamento_dia['DIA'] = list(map(clean, faturamento_dia['DIA']))
faturamento_dia['DIA'] = pd.Categorical(values = faturamento_dia['DIA'], 
                                        categories = ['SEGUNDA-FEIRA', 'TERÇA-FEIRA', 'QUARTA-FEIRA', 
                                                     'QUINTA-FEIRA', 'SEXTA-FEIRA', 'SÁBADO', 'DOMINGO'],
                                        ordered=True)

faturamento_dia = faturamento_dia.sort_values(by= 'DIA')

bar_chart = alt.Chart(faturamento_dia).mark_bar().encode(
    x=alt.X('DIA', title='Dia da Semana', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('FATURADO', title='Faturamento (R$)', 
            scale=alt.Scale(domain=[0, max(faturamento_dia['FATURADO']) * 1.3]))
).properties(
    title='Faturamento Total por Dia da Semana'
)

st.altair_chart(bar_chart, use_container_width=True)
