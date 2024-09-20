import pandas as pd
import altair as alt
import streamlit as st


st.set_page_config(page_title= "DashMulti", page_icon=":shark:", layout="wide")

data = pd.read_csv('galva.csv', sep = ';', decimal= ',')
data['DTMOV'] = pd.to_datetime(data.loc[:,'DTMOV'], dayfirst=True)
data = data.groupby(data['DTMOV'].dt.strftime('%m/%Y'))['QT'].sum().sort_values()
data = pd.DataFrame(data.astype(int))
data['DTMOV']= pd.to_datetime(data.index, format = '%m/%Y')

month_map = {
    '01': 'Janeiro',
    '02': 'Fevereiro',
    '03': 'Março',
    '04': 'Abril',
    '05': 'Maio',
    '06': 'Junho',
    '07': 'Julho',
    '08': 'Agosto',
    '09': 'Setembro',
    '10': 'Outubro',
    '11': 'Novembro',
    '12': 'Dezembro'
}

def convert_month_year(index_item):
    month, year = index_item.split('/')
    return f"{month_map[month]}, {year}"

data['TOOL'] = data.index.map(convert_month_year)
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
    x=alt.X('DTMOV:T', title='Meses',
            axis=alt.Axis(format='%m/%Y', labelAngle=0, labelOverlap=True, tickCount='month')), 
    y=alt.Y('QT', title='Quantidade Vendida', scale=alt.Scale(domain=[0, max(data['QT']) * 1.3])),
    tooltip=['TOOL', 'QT']
)

xrule = (alt.Chart()
    .mark_rule(color="white", strokeDash=[1, 6], size=1)
    .encode(x=alt.datum(alt.DateTime(year=2024, month=8)))
)


graph = graph + graph.mark_text(align='left', dx=2, dy=-15, size=10, color='white').encode(text='QT')
graph = graph + xrule

st.title('Análise de Vendas Produtos Galvano')
st.altair_chart(graph, use_container_width=True)
