import numpy as np
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
import pathlib

import plotly.graph_objects as go

from .constants import CATEGORY_COLORS

# Insira aqui o caminho para os dados processados!
#BASEPATH = './'
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

PREFIX_TITLE = 'Analisando vídeos da categoria: '

us_data = pd.read_csv(DATA_PATH.joinpath("USdata.csv"), parse_dates=['trending_date', 'publish_time'])

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
        dcc.Graph(id='formato-metricas', figure=display_fig())
    ], style={'display': 'inline-block', 'vertical-align': 'middle'})
])