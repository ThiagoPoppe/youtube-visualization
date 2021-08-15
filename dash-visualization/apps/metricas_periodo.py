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

category_colors = [f'hsl({h},50%,50%)' for h in np.linspace(0, 360, 30)]


week_data = us_data.copy()
week_data['week_day'] = week_data['trending_date'].dt.weekday
week_data['day_name'] = week_data['trending_date'].dt.day_name()

month_data = us_data.copy()
month_data['day'] = week_data['trending_date'].dt.day

year_data = us_data.copy()
year_data['month'] = year_data['trending_date'].dt.month
year_data['month_name'] = year_data['trending_date'].dt.month_name()

def display_fig1():

    trend_count = week_data.groupby(['category_name', 'week_day', 'day_name']).size().to_frame('trend_count')
    trend_count['percentage'] = trend_count.groupby(level=0).transform(lambda x: x / x.sum())

    # Ordenando pelo dia da semana (valor numérico) e dropando ele logo em seguida
    trend_count = trend_count.sort_index(level=[0,1])
    trend_count = trend_count.droplevel(1)

    traces = []
    categories = sorted(us_data['category_name'].unique())

    # Adicionando visualização com valor bruto
    for i in range(len(categories)):
        data = trend_count.loc[categories[i]]
        
        traces.append(go.Scatterpolar(
            r=data['trend_count'],
            theta=data.index.astype(str),
            fill='toself',
            marker_color=category_colors[i],
            name=categories[i],
            visible=True
        ))
        
    # Adicionando visualização com valor em escala logarítmica
    for i in range(len(categories)):
        data = trend_count.loc[categories[i]]
        
        traces.append(go.Scatterpolar(
            r=np.log10(1 + data['trend_count']),
            theta=data.index.astype(str),
            fill='toself',
            marker_color=category_colors[i],
            name=categories[i],
            visible=False
        ))

    # Adicionando visualização com porcentagem
    for i in range(len(categories)):
        data = trend_count.loc[categories[i]]
        
        traces.append(go.Scatterpolar(
            r=data['percentage'] * 100,
            theta=data.index.astype(str),
            fill='toself',
            marker_color=category_colors[i],
            name=categories[i],
            visible=False
        ))
        
    fig = go.Figure(traces)
    fig.update_layout(
        title='Número de vídeos em trend por dia da semana',
        updatemenus=[
            dict(
                active=0,
                buttons=list([
                    dict(
                        label='Escala Linear',
                        method='update',
                        args=[
                            {'visible': 16*[True] + 16*[False] + 16*[False]},
                            {'title': {'text': 'Número de vídeos em trend por dia da semana'}}
                        ]
                    ),
                    dict(
                        label='Escala Logarítmica',
                        method='update',
                        args=[
                            {'visible': 16*[False] + 16*[True] + 16*[False]},
                            {'title': {'text': 'Número de vídeos (log10) em trend por dia da semana'}}
                        ]
                    ),
                    dict(
                        label='Porcentagem (100%)',
                        method='update',
                        args=[
                            {'visible': 16*[False] + 16*[False] + 16*[True]},
                            {'title': {'text': 'Porcentagem (100%) de vídeos em trend por dia da semana'}}
                        ]
                    ),
                ])
            )
        ]
    )

    return fig



def display_fig2():

    trend_count = month_data.groupby(['category_name', 'day']).size().to_frame('trend_count')
    trend_count['percentage'] = trend_count.groupby(level=0).transform(lambda x: x / x.sum())

    traces = []
    categories = sorted(us_data['category_name'].unique())

    # Adicionando visualização com valor bruto
    for i in range(len(categories)):
        data = trend_count.loc[categories[i]]
        
        traces.append(go.Scatterpolar(
            r=data['trend_count'],
            theta=data.index.astype(str),
            fill='toself',
            marker_color=category_colors[i],
            name=categories[i],
            visible=True
        ))
        
    # Adicionando visualização com valor em escala logarítmica
    for i in range(len(categories)):
        data = trend_count.loc[categories[i]]
        
        traces.append(go.Scatterpolar(
            r=np.log10(1 + data['trend_count']),
            theta=data.index.astype(str),
            fill='toself',
            marker_color=category_colors[i],
            name=categories[i],
            visible=False
        ))

    # Adicionando visualização com porcentagem
    for i in range(len(categories)):
        data = trend_count.loc[categories[i]]
        
        traces.append(go.Scatterpolar(
            r=data['percentage'] * 100,
            theta=data.index.astype(str),
            fill='toself',
            marker_color=category_colors[i],
            name=categories[i],
            visible=False
        ))
        
    fig = go.Figure(traces)
    fig.update_layout(
        title='Número de vídeos em trend por dia do mês',
        updatemenus=[
            dict(
                active=0,
                buttons=list([
                    dict(
                        label='Escala Linear',
                        method='update',
                        args=[
                            {'visible': 16*[True] + 16*[False] + 16*[False]},
                            {'title': {'text': 'Número de vídeos em trend por dia do mês'}}
                        ]
                    ),
                    dict(
                        label='Escala Logarítmica',
                        method='update',
                        args=[
                            {'visible': 16*[False] + 16*[True] + 16*[False]},
                            {'title': {'text': 'Número de vídeos (log10) em trend por dia do mês'}}
                        ]
                    ),
                    dict(
                        label='Porcentagem (100%)',
                        method='update',
                        args=[
                            {'visible': 16*[False] + 16*[False] + 16*[True]},
                            {'title': {'text': 'Porcentagem (100%) de vídeos em trend por dia do mês'}}
                        ]
                    ),
                ])
            )
        ]
    )
    return fig

def display_fig3():
    trend_count = year_data.groupby(['category_name', 'month', 'month_name']).size().to_frame('trend_count')
    trend_count['percentage'] = trend_count.groupby(level=0).transform(lambda x: x / x.sum())

    # Ordenando pelo mês (valor numérico) e dropando ele logo em seguida
    trend_count = trend_count.sort_index(level=[0,1])
    trend_count = trend_count.droplevel(1)

    traces = []
    categories = sorted(us_data['category_name'].unique())
    months = ['January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December']

    # Adicionando visualização com valor bruto
    for i in range(len(categories)):
        data = trend_count.loc[categories[i]].reindex(months)
        
        traces.append(go.Scatter(
            x=data.index.astype(str),
            y=data['trend_count'],
            marker_color=category_colors[i],
            name=categories[i],
            visible=True
        ))
        
    # Adicionando visualização com valor em escala logarítmica
    for i in range(len(categories)):
        data = trend_count.loc[categories[i]].reindex(months)
        
        traces.append(go.Scatter(
            x=data.index.astype(str),
            y=np.log10(1 + data['trend_count']),
            marker_color=category_colors[i],
            name=categories[i],
            visible=False
        ))

    # Adicionando visualização com porcentagem
    for i in range(len(categories)):
        data = trend_count.loc[categories[i]].reindex(months)
        
        traces.append(go.Scatter(
            x=data.index.astype(str),
            y=data['percentage'] * 100,
            marker_color=category_colors[i],
            name=categories[i],
            visible=False
        ))
        
    fig = go.Figure(traces)
    fig.update_layout(
        title='Número de vídeos em trend por mês do ano',
        updatemenus=[
            dict(
                active=0,
                buttons=list([
                    dict(
                        label='Escala Linear',
                        method='update',
                        args=[
                            {'visible': 16*[True] + 16*[False] + 16*[False]},
                            {'title': {'text': 'Número de vídeos em trend por mês do ano'}}
                        ]
                    ),
                    dict(
                        label='Escala Logarítmica',
                        method='update',
                        args=[
                            {'visible': 16*[False] + 16*[True] + 16*[False]},
                            {'title': {'text': 'Número de vídeos (log10) em trend por mês do ano'}}
                        ]
                    ),
                    dict(
                        label='Porcentagem (100%)',
                        method='update',
                        args=[
                            {'visible': 16*[False] + 16*[False] + 16*[True]},
                            {'title': {'text': 'Porcentagem (100%) de vídeos em trend por mês do ano'}}
                        ]
                    ),
                ])
            )
        ]
    )

    return fig

layout = html.Div([
    html.H1('Métricas por período', style={"textAlign": "center"}),
    dcc.Graph(id='my-graph', figure=display_fig1()),
    dcc.Graph(id='my-graph', figure=display_fig2()),
    dcc.Graph(id='my-graph', figure=display_fig3()),
])