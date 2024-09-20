import pandas as pd
import numpy as np
import datetime as dt


def clean(x):
    return x.strip()

def loaddata(caminho):
    data = pd.read_csv(caminho, sep = ";")
    data['DATA'] = pd.to_datetime(data.loc[:,'DATA'], dayfirst=True)
    data['FATURADO'] = data['FATURADO'].str.replace('.', '').str.replace(',', '.').astype(float)
    data['CUSTO'] = data['CUSTO'].str.replace('.' , '').str.replace(',', '.').astype(float)
    data = data.sort_values(by = 'DATA')
    return data

def fatudia(data):
    faturamento_dia = data.groupby('DIA')['FATURADO'].sum().reset_index()
    
    faturamento_dia['DIA'] = list(map(clean, faturamento_dia['DIA']))
    faturamento_dia['DIA'] = pd.Categorical(values = faturamento_dia['DIA'], 
                                            categories = ['SEGUNDA-FEIRA', 'TERÇA-FEIRA', 'QUARTA-FEIRA', 
                                                     'QUINTA-FEIRA', 'SEXTA-FEIRA', 'SÁBADO', 'DOMINGO'],
                                            ordered=True)

    faturamento_dia = faturamento_dia.sort_values(by= 'DIA')
    x = faturamento_dia.loc[(faturamento_dia['DIA'] == 'SÁBADO') | (faturamento_dia['DIA'] == 'SEGUNDA-FEIRA')]['FATURADO'].sum()
    faturamento_dia.loc[faturamento_dia['DIA'] == 'SEGUNDA-FEIRA', 'FATURADO'] = x
    faturamento_dia.drop( index = faturamento_dia.loc[faturamento_dia['DIA'] == 'SÁBADO'].index, inplace = True)
    return faturamento_dia