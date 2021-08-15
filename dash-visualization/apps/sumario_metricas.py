from os.path import join as ospj

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pathlib
from app import app

import plotly.graph_objects as go
import plotly

# Insira aqui o caminho para os dados processados!
#BASEPATH = './'
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

us_data = pd.read_csv(DATA_PATH.joinpath("USdata.csv"), parse_dates=['trending_date', 'publish_time'])

modes = ['linear', 'log10']
metrics = ['views', 'likes', 'dislikes', 'comment_count']

grouped_data = us_data.groupby(['trending_date','category_name'])[metrics]
grouped_data = grouped_data.sum()
grouped_data = grouped_data.reset_index()

category_colors = [f'hsl({h},50%,50%)' for h in np.linspace(0, 360, 30)]

def get_visibility(idx, n=8, n_categories=16):
    """ Função auxiliar para retornar uma lista de visibilidade para os filtros """
    
    visibility = []
    booleans = [(i == idx) for i in range(n)]
    
    for b in booleans:
        visibility.extend([b] * n_categories)
    
    return visibility


## Criando trace para cada plot (serão 8 pares (mode, metric) no total)
traces = []
categories = sorted(us_data['category_name'].unique())

for mode in modes:
    for metric in metrics:
        for i in range(len(categories)):
            data = grouped_data[grouped_data['category_name'] == categories[i]]
            traces.append(go.Bar(
                name = categories[i],
                marker_color = category_colors[i],
                x = data['trending_date'],
                y = data[metric] if mode == 'linear' else np.log10(1+data[metric]),
                visible = True if mode == 'linear' and metric == 'views' else False
            ))
            
fig = go.Figure(data=traces[::-1])


## Definindo botões para filtro 
idx = 0    
buttons = []

for mode in modes:
    for metric in metrics:
        buttons.append({
            'label': f'{metric} - {mode}',
            'method': 'update',
            'args': [{'visible': get_visibility(idx)}]
        })
        
        idx += 1

fig.update_layout(updatemenus=[
    dict(
        x = -0.15,
        active = 0,
        showactive = True,
        buttons = buttons
    )
])

## Definindo outras propriedades de layout
fig.update_layout(
    title='Somatório diário das métricas por categoria',
    xaxis_title='trending date',
    barmode='stack'
)

    
layout = html.Div([
    html.H1('Somatório diário das métricas por categoria', style={"textAlign": "center"}),
    dcc.Graph(id='my-graph', figure=fig),
])