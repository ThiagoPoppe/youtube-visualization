import numpy as np
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import pathlib
import plotly

import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

from .constants import CATEGORY_COLORS

# Insira aqui o caminho para os dados processados!
#BASEPATH = './'
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

PREFIX_TITLE = 'Analisando vídeos da categoria: '

us_data = pd.read_csv(DATA_PATH.joinpath("USdata.csv"), parse_dates=['trending_date', 'publish_time'])
us_data = us_data.groupby(['category_name', 'video_id']).apply(lambda df: df.iloc[-1])
us_data = us_data.reset_index(drop=True)

categories = us_data[['category_name']].drop_duplicates().reset_index(drop=True)
categories['category_id'] = range(1, len(categories)+1)

categories = categories.sort_values('category_id', ascending=False)
categories = categories[['category_id', 'category_name']]

us_data = us_data.drop('category_id', axis=1)
us_data = us_data.merge(categories)

def display_full_fig():
    fig = px.parallel_coordinates(
        us_data,
        color='category_id',
        dimensions=['views', 'likes', 'dislikes', 'comment_count', 'category_id'],
        color_continuous_scale=plotly.colors.sequential.Plasma
    )

    return fig

def display_category_table():
    fig = ff.create_table(categories)
    fig.update_layout(
        width=300,
        height=400
    )

    return fig

def display_fig():
    categories = sorted(us_data['category_name'].unique())
    visibilites = [v.astype(bool) for v in np.eye(len(categories))]

    traces = []
    for i in range(0, len(categories)):
        data = us_data[us_data['category_name'] == categories[i]]
        traces.append(go.Parcoords(
            line=dict(color=CATEGORY_COLORS[i]),
            dimensions=[
                dict(label='views', values=data['views']),
                dict(label='likes', values=data['likes']),
                dict(label='dislikes', values=data['dislikes']),
                dict(label='comment_count', values=data['comment_count'])
            ],
            visible = True if i == 0 else False
        ))
        
    fig = go.Figure(data=traces)

    fig.update_layout(
        width=1200,
        height=600,
        title=dict(
            x=0.015,
            y=0.98,
            font=dict(size=20),
            text=PREFIX_TITLE + categories[0],
        ),

        updatemenus=[
            dict(
                x=-0.05,
                active=0,
                showactive=True,
                buttons=list([
                    dict(
                        label=categories[i],
                        method='update',
                        args=[
                            dict(visible=visibilites[i]),
                            dict(
                                title=dict(
                                    x=0.015,
                                    y=0.98,
                                    font=dict(size=20),
                                    text=PREFIX_TITLE + categories[i],
                                ),
                            )
                        ]
                    )
                    for i in range(0, len(categories))
                ]),
            ),
        ]
    )

    return fig
    
layout = html.Div([
    html.H3('Formato das Métricas'),
    html.P('Coloque aqui uma breve descrição da visualização, como interagir e insights.'),
    html.Div([
        html.Div([
            dcc.Graph(id='metricas-geral', figure=display_full_fig(), style={'width': '100%'}),
            dcc.Graph(id='categorias-nome', figure=display_category_table())
        ], style={'display': 'flex', 'flex-direction': 'row'}),
        dcc.Graph(id='formato-metricas', figure=display_fig())
    ], style={'display': 'inline-block', 'vertical-align': 'middle'})
])