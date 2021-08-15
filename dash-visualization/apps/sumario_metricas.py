import numpy as np
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import pathlib

import plotly.graph_objects as go

# Insira aqui o caminho para os dados processados!
#BASEPATH = './'
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

PREFIX_TITLE = 'Métrica selecionada: '

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
## Para termos as barras ordenadas pelo nome das categorias, devemos inserir
## as categorias de trás para frente
traces = []
categories = sorted(us_data['category_name'].unique())[::-1]

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

## Definindo botões para filtro 
idx = 0    
buttons = []

for mode in modes:
    for metric in metrics:
        buttons.append({
            'label': f'{metric} - {mode}',
            'method': 'update',
            'args': [
                dict(visible=get_visibility(idx)),
                dict(title=dict(
                    x=0.015,
                    y=0.98,
                    font=dict(size=20),
                    text=PREFIX_TITLE + metric,
                ))
            ]
        })
        
        idx += 1

fig = go.Figure(data=traces)

## Definindo outras propriedades de layout
fig.update_layout(
    width=1200,
    height=600,
    title=dict(
        x=0.015,
        y=0.98,
        font=dict(size=20),
        text=PREFIX_TITLE + metrics[0],
    ),
    yaxis_title='Valor da métrica',
    xaxis_title='Trending Date',
    barmode='stack',

    updatemenus=[
         dict(
            x=-0.1,
            active=0,
            showactive=True,
            buttons=buttons
        )
    ]
)

layout = html.Div([
    html.H3('Somatório diário das métricas por categoria'),
    html.P('Selecione uma métrica e escala'),
    html.Div([
        dcc.Graph(id='sumario-metricas', figure=fig)
    ], style={'display': 'inline-block', 'vertical-align': 'middle'})
])