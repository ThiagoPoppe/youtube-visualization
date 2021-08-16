import pathlib

import numpy as np
import pandas as pd
import plotly.graph_objects as go

import dash_core_components as dcc
import dash_html_components as html

from .constants import CATEGORY_COLORS

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

us_data = pd.read_csv(DATA_PATH.joinpath("USdata.csv"), parse_dates=['trending_date', 'publish_time'])

def display_views_ranking():
    num_views = us_data.groupby('category_name')['views'].sum()
    num_views = num_views.sort_values()

    fig = go.Figure()

    # Adicionando plot para número de views
    fig.add_trace(go.Bar(
        x=num_views.values,
        y=num_views.index,
        name='Número de views',
        orientation='h',
        marker_color=CATEGORY_COLORS,
        visible=True
    ))

    # Adicionando plot para número de views (porcentagem)
    fig.add_trace(go.Bar(
        x=100 * (num_views.values / sum(num_views.values)),
        y=num_views.index,
        name='Porcentagem de views (100%)',
        orientation='h',
        marker_color=CATEGORY_COLORS,
        visible=False
    ))

    fig.update_layout(
        title='Comparação do número de views em cada categoria',
        xaxis_title='Número de views',
        yaxis_title='Categorias',
        width=1200,
        height=600,
    
        updatemenus=list([
            dict(
                x=-0.2,
                active=0,
                buttons=list([
                    dict(
                        label='Escala Linear',
                        method='update',
                        args=[
                            dict(visible=[True, False]),
                            dict(xaxis=dict(
                                type='linear',
                                title='Número de views'
                            ))
                        ]
                    ),
                    dict(
                        label='Escala Logarítimica',
                        method='update',
                        args=[
                            dict(visible=[True, False]),
                            dict(xaxis=dict(
                                type='log',
                                title='Número de views (log10)'
                            ))
                        ]
                    ),
                    dict(
                        label='Porcentagem',
                        method='update',
                        args=[
                            dict(visible=[False, True]),
                            dict(xaxis=dict(
                                type='linear',
                                title='Porcentagem de views (100%)'
                            ))
                        ]
                    ),  
                ])
            )
        ])
    )

    return fig

def display_likes_ranking():
    num_likes = us_data.groupby('category_name')['likes'].sum()
    num_likes = num_likes.sort_values()

    fig = go.Figure()

    # Adicionando plot para número de likes
    fig.add_trace(go.Bar(
        x=num_likes.values,
        y=num_likes.index,
        name='Número de likes',
        orientation='h',
        marker_color=CATEGORY_COLORS,
        visible=True
    ))

    # Adicionando plot para número de likes (porcentagem)
    fig.add_trace(go.Bar(
        x=100 * (num_likes.values / sum(num_likes.values)),
        y=num_likes.index,
        name='Porcentagem de likes (100%)',
        orientation='h',
        marker_color=CATEGORY_COLORS,
        visible=False
    ))

    fig.update_layout(
        title='Comparação do número de likes em cada categoria',
        xaxis_title='Número de likes',
        yaxis_title='Categorias',
        width=1200,
        height=600,
    
        updatemenus=list([
            dict(
                x=-0.2,
                active=0,
                buttons=list([
                    dict(
                        label='Escala Linear',
                        method='update',
                        args=[
                            dict(visible=[True, False]),
                            dict(xaxis=dict(
                                type='linear',
                                title='Número de likes'
                            ))
                        ]
                    ),
                    dict(
                        label='Escala Logarítimica',
                        method='update',
                        args=[
                            dict(visible=[True, False]),
                            dict(xaxis=dict(
                                type='log',
                                title='Número de likes (log10)'
                            ))
                        ]
                    ),
                    dict(
                        label='Porcentagem',
                        method='update',
                        args=[
                            dict(visible=[False, True]),
                            dict(xaxis=dict(
                                type='linear',
                                title='Porcentagem de likes (100%)'
                            ))
                        ]
                    ),  
                ])
            )
        ])
    )

    return fig

def display_dislikes_ranking():
    num_dislikes = us_data.groupby('category_name')['dislikes'].sum()
    num_dislikes = num_dislikes.sort_values()

    fig = go.Figure()

    # Adicionando plot para número de dislikes
    fig.add_trace(go.Bar(
        x=num_dislikes.values,
        y=num_dislikes.index,
        name='Número de dislikes',
        orientation='h',
        marker_color=CATEGORY_COLORS,
        visible=True
    ))

    # Adicionando plot para número de dislikes (porcentagem)
    fig.add_trace(go.Bar(
        x=100 * (num_dislikes.values / sum(num_dislikes.values)),
        y=num_dislikes.index,
        name='Porcentagem de dislikes (100%)',
        orientation='h',
        marker_color=CATEGORY_COLORS,
        visible=False
    ))

    fig.update_layout(
        title='Comparação do número de dislikes em cada categoria',
        xaxis_title='Número de dislikes',
        yaxis_title='Categorias',
        width=1200,
        height=600,
    
        updatemenus=list([
            dict(
                x=-0.2,
                active=0,
                buttons=list([
                    dict(
                        label='Escala Linear',
                        method='update',
                        args=[
                            dict(visible=[True, False]),
                            dict(xaxis=dict(
                                type='linear',
                                title='Número de dislikes'
                            ))
                        ]
                    ),
                    dict(
                        label='Escala Logarítimica',
                        method='update',
                        args=[
                            dict(visible=[True, False]),
                            dict(xaxis=dict(
                                type='log',
                                title='Número de dislikes (log10)'
                            ))
                        ]
                    ),
                    dict(
                        label='Porcentagem',
                        method='update',
                        args=[
                            dict(visible=[False, True]),
                            dict(xaxis=dict(
                                type='linear',
                                title='Porcentagem de dislikes (100%)'
                            ))
                        ]
                    ),  
                ])
            )
        ])
    )

    return fig

def display_comments_ranking():
    num_comments = us_data.groupby('category_name')['comment_count'].sum()
    num_comments = num_comments.sort_values()

    fig = go.Figure()

    # Adicionando plot para número de comentários
    fig.add_trace(go.Bar(
        x=num_comments.values,
        y=num_comments.index,
        name='Número de comentários',
        orientation='h',
        marker_color=CATEGORY_COLORS,
        visible=True
    ))

    # Adicionando plot para número de comentários (porcentagem)
    fig.add_trace(go.Bar(
        x=100 * (num_comments.values / sum(num_comments.values)),
        y=num_comments.index,
        name='Porcentagem de comentários (100%)',
        orientation='h',
        marker_color=CATEGORY_COLORS,
        visible=False
    ))

    fig.update_layout(
        title='Comparação do número de comentários em cada categoria',
        xaxis_title='Número de comentários',
        yaxis_title='Categorias',
        width=1200,
        height=600,
    
        updatemenus=list([
            dict(
                x=-0.2,
                active=0,
                buttons=list([
                    dict(
                        label='Escala Linear',
                        method='update',
                        args=[
                            dict(visible=[True, False]),
                            dict(xaxis=dict(
                                type='linear',
                                title='Número de comentários'
                            ))
                        ]
                    ),
                    dict(
                        label='Escala Logarítimica',
                        method='update',
                        args=[
                            dict(visible=[True, False]),
                            dict(xaxis=dict(
                                type='log',
                                title='Número de comentários (log10)'
                            ))
                        ]
                    ),
                    dict(
                        label='Porcentagem',
                        method='update',
                        args=[
                            dict(visible=[False, True]),
                            dict(xaxis=dict(
                                type='linear',
                                title='Porcentagem de comentários (100%)'
                            ))
                        ]
                    ),  
                ])
            )
        ])
    )

    return fig

layout = html.Div([
    html.H3('Ranking das métricas'),
    html.P('Coloque aqui uma breve descrição da visualização, como interagir e insights.'),
    html.Div([
        dcc.Graph(id='views-ranking', figure=display_views_ranking()),
        dcc.Graph(id='likes-ranking', figure=display_likes_ranking()),
        dcc.Graph(id='dislikes-ranking', figure=display_dislikes_ranking()),
        dcc.Graph(id='comments-ranking', figure=display_comments_ranking())   
    ], style={'display': 'inline-block', 'vertical-align': 'middle'})
])