from dash_core_components.Graph import Graph
from dash_html_components.Div import Div
import plotly
import pathlib

import numpy as np
import pandas as pd

import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

us_data = pd.read_csv(DATA_PATH.joinpath("USdata.csv"), parse_dates=['trending_date', 'publish_time'])

category_colors = [f'hsl({h},50%,50%)' for h in np.linspace(0, 360, 30)]

category_counts = us_data.groupby('category_name').size()
category_counts = category_counts.to_frame('trend_count')
category_counts['percentage'] = category_counts['trend_count'] / category_counts['trend_count'].sum()
category_counts = category_counts.sort_values('trend_count', ascending=False)

fig = plotly.subplots.make_subplots(specs=[[{"secondary_y": True}]])

# Adicionando gráfico de barras com a contagem de trend em escala linear
fig.add_trace(
    go.Bar(
        x=category_counts.index,
        y=category_counts['trend_count'],
        marker_color=category_colors,
        name='Número de vídeos',
        visible=True
    ),
    secondary_y=False
)

# Adicionando gráfico de barras com a contagem de trend em escala logarítimca
fig.add_trace(
    go.Bar(
        x=category_counts.index,
        y=np.log10(1 + category_counts['trend_count']),
        marker_color=category_colors,
        name='Número de vídeos (log10)',
        visible=False
    ),
    secondary_y=False
)

# Adicionando gráfico de barras com a contagem de trend em porcentagem (100%)
fig.add_trace(
    go.Bar(
        x=category_counts.index,
        y=category_counts['percentage'] * 100,
        marker_color=category_colors,
        name='Porcentagem de vídeos (100%)',
        visible=False
    ),
    secondary_y=False
)

# Adicionando gráfico de linha para representar a porcentagem acumulada (Gráfico de Pareto)
fig.add_trace(
    go.Scatter(
        x=category_counts.index,
        y=np.cumsum(category_counts['percentage']),
        name='Porcentagem acumulada',
        visible=True
    ),
    secondary_y=True
)

fig.update_layout(
    xaxis_title='Categorias',
    yaxis_title='Número de vídeos',
    width=1200,
    height=600,

    updatemenus=[
        dict(
            x=-0.1,
            active=0,
            buttons=list([
                dict(
                    label='Escala Linear',
                    method='update',
                    args=[
                        {'visible': [True, False, False, True]},
                        {'yaxis': {'title': 'Número de vídeos'}}
                    ]
                ),
                dict(
                    label='Escala Logarítmica',
                    method='update',
                    args=[
                        {'visible': [False, True, False, True]},
                        {'yaxis': {'title': 'Número de vídeos (log10)'}}
                    ]
                ),
                dict(
                    label='Porcentagem',
                    method='update',
                    args=[
                        {'visible': [False, False, True, True]},
                        {'yaxis': {'title': 'Porcentagem (100%)'}}
                    ]
                )
            ])
        )
    ]
)

    
layout = html.Div([
    html.H3('Número de vídeos em trend por categoria'),
    html.P('Selecione uma escala'),
    html.Div([
        dcc.Graph(id='trend-categoria', figure=fig)
    ], style={'display': 'inline-block', 'vertical-align': 'middle'})
])