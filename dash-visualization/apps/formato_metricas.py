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

def display_fig():
    categories = sorted(us_data['category_name'].unique())
    visibilites = [v.astype(bool) for v in np.eye(len(categories))]

    traces = []
    for i in range(0, len(categories)):
        data = us_data[us_data['category_name'] == categories[i]]
        traces.append(go.Parcoords(
            line=dict(color=category_colors[i]),
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
        title='Métricas dos vídeos dos Estados Unidos',
        updatemenus=[
            dict(
                active=0,
                showactive=True,
                buttons=list([
                    dict(label=categories[i], method='update', args=[{'visible': visibilites[i]}])
                    for i in range(0, len(categories))
                ]),
                x=1.4
            ),
        ]
    )

    # fig.show()
    return fig
    
layout = html.Div([
    html.H1('Métricas dos vídeos dos Estados Unidos', style={"textAlign": "center"}),
    dcc.Graph(id='my-graph', figure=display_fig()),
])