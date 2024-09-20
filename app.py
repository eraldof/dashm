import utils as ut
import streamlit as st
import altair as alt
import datetime as dt


st.set_page_config(page_title= "DashMulti", page_icon=":shark:", layout="wide")

data = ut.loaddata('data.csv')
faturamento_dia = ut.fatudia(data)

graph = alt.Chart(data).mark_area(line={'color' : 'white'},
    point={'color' : 'darkblue'},
    color=alt.Gradient(
        gradient='linear',
        stops=[alt.GradientStop(color='black', offset=0),
               alt.GradientStop(color='darkblue', offset=1)],
        x1=1,
        x2=1,
        y1=1,
        y2=0
    )
).encode(
    x=alt.X('DATA:T', title='Meses',
            axis=alt.Axis(format='%d', labelAngle=0, labelOverlap=True, tickCount='day')), 
    y=alt.Y('FATURADO', title='Quantidade Vendida', scale=alt.Scale(domain=[0, max(data['FATURADO']) * 1.3])),
    tooltip=['DIA', 'FATURADO']
)


st.title('Análise do Faturamento')
st.altair_chart(graph, use_container_width=True)

st.divider()


st.title("Métricas Diárias")

um, dois = st.columns ([1,5])

with um:
    d = st.date_input("Selecione uma data:", format= 'DD/MM/YYYY', 
                          min_value= dt.date(2024, 9, 1), max_value = dt.date(2024, 9, 30))
    t = data[data['DATA'] == str(d)]


col1, col2, col3 = st.columns(3)

with col1:
    try:
        st.metric(label="FATURAMENTO", value = str(t.iloc[0]['FATURADO']) + ' R$')
    except:
        st.metric(label="FATURAMENTO", value = '--')


with col2: 
    try:
        margem = float(round(((t['FATURADO'] - t['CUSTO']) / t['FATURADO']) * 100, 2))
        st.metric(label="MARGEM", value = str(margem) + ' %')
    except:
        st.metric(label="MARGEM", value = '--')

with col3:
    try:
        st.metric(label="MIX", value = t.iloc[0]['MIX'])
    except:
        st.metric(label="MIX", value = '--')


st.divider() 


st.title('Análise do Faturamento por Dia da Semana')

bar_chart = alt.Chart(faturamento_dia).mark_bar(
    color = alt.Gradient(
        gradient='linear',
        stops=[alt.GradientStop(color='black', offset=0),
               alt.GradientStop(color='darkblue', offset=1)],
        x1=1,
        x2=1,
        y1=1,
        y2=0
    )
).encode(
    x=alt.X('DIA', title='Dia da Semana', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('FATURADO', title='Faturamento (R$)', 
            scale=alt.Scale(domain=[0, max(faturamento_dia['FATURADO']) * 1.3]))
).properties(
    title='Faturamento Total por Dia da Semana'
)

st.altair_chart(bar_chart, use_container_width=True)





