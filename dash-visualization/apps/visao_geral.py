import pathlib

import plotly
import plotly.subplots

import numpy as np
import pandas as pd

import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html

from .constants import CATEGORY_COLORS

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

us_data = pd.read_csv(DATA_PATH.joinpath("USdata.csv"), parse_dates=['trending_date', 'publish_time'])

def display_grafico_pareto():
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
            marker_color=CATEGORY_COLORS,
            name='Número de vídeos',
            visible=True
        ),
        secondary_y=False
    )

    # Adicionando gráfico de barras com a contagem de trend em porcentagem (100%)
    fig.add_trace(
        go.Bar(
            x=category_counts.index,
            y=category_counts['percentage'] * 100,
            marker_color=CATEGORY_COLORS,
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
        title='Número de vídeos em trend por categoria',
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
                            {'visible': [True, False, True]},
                            {'yaxis': {'type': 'linear', 'title': 'Número de vídeos'}}
                        ]
                    ),
                    dict(
                        label='Escala Logarítmica',
                        method='update',
                        args=[
                            {'visible': [True, False, True]},
                            {'yaxis': {'type': 'log', 'title': 'Número de vídeos (log10)'}}
                        ]
                    ),
                    dict(
                        label='Porcentagem',
                        method='update',
                        args=[
                            {'visible': [False, True, True]},
                            {'yaxis': {'type': 'linear', 'title': 'Porcentagem de vídeos (100%)'}}
                        ]
                    )
                ])
            )
        ]
    )

    return fig

def display_number_of_videos_ranking():
    video_counts = us_data.groupby('category_name')['title'].unique()
    for i in range(len(video_counts)):
        video_counts.iloc[i] = len(video_counts.iloc[i])

    video_counts = video_counts.sort_values(ascending=True)

    video_counts_percentage = 100 * (video_counts / sum(video_counts))
    video_counts_percentage = video_counts_percentage.sort_values(ascending=True)

    fig = go.Figure()
    
    # Adicionando plot com número de vídeos por categoria
    fig.add_trace(go.Bar(
        x=video_counts.values,
        y=video_counts.index,
        name='Número de vídeos',
        orientation='h',
        marker_color=CATEGORY_COLORS,
        visible=True
    ))

    # Adicionando plot com porcentagem do número de vídeos por categoria
    fig.add_trace(go.Bar(
        x=video_counts_percentage.values,
        y=video_counts_percentage.index,
        name='Porcentagem de vídeos (100%)',
        orientation='h',
        marker_color=CATEGORY_COLORS,
        visible=False
    ))

    fig.update_layout(
        title='Ranking de categorias com mais vídeos',
        yaxis_title='Categorias',
        xaxis_title='Número de vídeos',
        width=1200,
        height=600,

        updatemenus=[
            dict(
                x=-0.2,
                active=0,
                buttons=[
                    dict(
                        label='Escala Linear',
                        method='update',
                        args=[
                            dict(visible=[True, False]),
                            dict(xaxis=dict(type='linear', title='Número de vídeos'))
                        ]
                    ),
                    dict(
                        label='Escala Logarítmica',
                        method='update',
                        args=[
                            dict(visible=[True, False]),
                            dict(xaxis=dict(type='log', title='Número de vídeos (log10)'))
                        ]
                    ),
                    dict(
                        label='Porcentagem',
                        method='update',
                        args=[
                            dict(visible=[False, True]),
                            dict(xaxis=dict(type='linear', title='Porcentagem de vídeos (100%)'))
                        ]
                    )
                ]
            )
        ]
    )

    return fig

def display_most_watched_videos():
    top10_view = []
    top10_view_name = us_data.sort_values(by='views', ascending=False)['title'].unique().tolist()[:10]
    for i in range(len(top10_view_name)):
        top10_view.append(us_data[us_data['title']==top10_view_name[i]]['views'].sort_values(ascending=False)[:1].values[0])

    top10_view = np.array(top10_view)

    fig = go.Figure()

    # Adicionando plot com o número de views dos top 10 vídeos
    fig.add_trace(go.Bar(
        x=top10_view[::-1],
        y=top10_view_name[::-1],
        name='Número de views',
        orientation='h',
        marker_color=CATEGORY_COLORS,
        visible=True
    ))

    # Adicionando plot com o número de views dos top 10 vídeos (porcentagem)
    fig.add_trace(go.Bar(
        x=100 * (top10_view[::-1] / sum(top10_view)),
        y=top10_view_name[::-1],
        name='Porcentagem de views (100%)',
        orientation='h',
        marker_color=CATEGORY_COLORS,
        visible=False
    ))

    fig.update_layout(
        title='Top 10 vídeos mais vistos',
        xaxis_title='Número de views do vídeo',
        yaxis_title='Nome do vídeo',
        width=1200,
        height=600,

        updatemenus = list([
            dict(
                x=-0.8,
                active=0,
                buttons=list([
                    dict(
                        label='Escala Linear',
                        method='update',
                        args=[
                            dict(visible=[True, False]),
                            dict(xaxis=dict(type='linear', title='Número de views'))
                        ]
                    ),
                    dict(
                        label='Escala Logarítmica',
                        method='update',
                        args=[
                            dict(visible=[True, False]),
                            dict(xaxis=dict(type='log', title='Número de views (log10)'))
                        ]
                    ),
                    dict(
                        label='Porcentagem',
                        method='update',
                        args=[
                            dict(visible=[False, True]),
                            dict(xaxis=dict(type='linear', title='Porcentagem de views (100%)'))
                        ]
                    )
                ])
            )
        ])
    )

    return fig

layout = html.Div([
    html.H3('Visão Geral'),
    html.P('Coloque aqui uma breve descrição da visualização, como interagir e insights.'),
    html.Div([
        dcc.Graph(id='grafico-pareto', figure=display_grafico_pareto()),
        dcc.Graph(id='number-videos-ranking', figure=display_number_of_videos_ranking()),
        dcc.Graph(id='most-watched-videos', figure=display_most_watched_videos())
    ], style={'display': 'inline-block', 'vertical-align': 'middle'})
])