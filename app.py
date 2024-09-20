import utils as ut
import streamlit as st
import altair as alt
import datetime as dt


st.set_page_config(page_title= "DashMulti", page_icon=":shark:", layout="wide")

data = ut.loaddata('data.csv')
faturamento_dia = ut.fatudia(data)


line_chart = alt.Chart(data).mark_line(point=True).encode(
    x=alt.X('DATA:T', title='Dia', axis=alt.Axis(format='%d/%m')), 
    y=alt.Y('FATURADO', title='Faturamento (R$)', scale=alt.Scale(domain=[0, max(data['FATURADO']) * 1.3])),  
    tooltip=['DATA:T', 'DIA', 'FATURADO']  
).properties(
    title='Evolução Diária do Faturamento'  
)

st.title('Análise do Faturamento')
st.altair_chart(line_chart, use_container_width=True)

st.divider()


st.title("Métricas Diárias")

um, dois = st.columns ([1,8])

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

bar_chart = alt.Chart(faturamento_dia).mark_bar().encode(
    x=alt.X('DIA', title='Dia da Semana', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('FATURADO', title='Faturamento (R$)', 
            scale=alt.Scale(domain=[0, max(faturamento_dia['FATURADO']) * 1.3]))
).properties(
    title='Faturamento Total por Dia da Semana'
)

st.altair_chart(bar_chart, use_container_width=True)
