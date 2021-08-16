import pathlib

import numpy as np
import pandas as pd

import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html

from app import app
from .constants import CATEGORY_COLORS

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

us_data = pd.read_csv(DATA_PATH.joinpath("USdata.csv"), parse_dates=['trending_date', 'publish_time'])

def display_boxplot_number_trend():
    trend_count = us_data.groupby(['title', 'category_name']).size()
    trend_count = trend_count.reset_index(name='trend_count')
    trend_count = trend_count[trend_count['trend_count'] > 0]

    categories = sorted(trend_count['category_name'].unique())
    # Each box is represented by a dict that contains the data, the type, and the colour.
    # Use list comprehension to describe N boxes, each with a different colour and with different randomly generated data:
    fig = go.Figure(data=[go.Box(
        y=trend_count[trend_count['category_name'] == categories[i]]['trend_count'],
        marker_color=CATEGORY_COLORS[i],
        name= categories[i],
        ) for i in range(0, len(categories))])

    # format the layout
    fig.update_layout(
        title='Número de vídeos que entraram em trend mais de uma vez',
        xaxis=dict(title='Categorias', showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(title='Quantidade de dias em trend', zeroline=False, gridcolor='white'),
        plot_bgcolor='rgb(233,233,233)',
        width=1200,
        height=600
    )

    return fig

def display_boxplot_max_trend_window():
    def biggest_window_trend_time(df):
        max_window = 1
        diff1 = df['trending_date'].diff() == pd.Timedelta('1D')
        
        counter = 0
        for value in diff1:
            counter = counter + 1 if value else 1
            max_window = max(max_window, counter)
            
        return max_window

    max_trend_window = us_data.groupby(['title', 'category_name']).apply(biggest_window_trend_time)
    max_trend_window = max_trend_window.to_frame('max_trend_window')
    max_trend_window = max_trend_window.reset_index()

    categories = sorted(max_trend_window['category_name'].unique())
    # Each box is represented by a dict that contains the data, the type, and the colour.
    # Use list comprehension to describe N boxes, each with a different colour and with different randomly generated data:
    fig = go.Figure(data=[go.Box(
        y=max_trend_window[max_trend_window['category_name'] == categories[i]]['max_trend_window'],
        marker_color=CATEGORY_COLORS[i],
        name= categories[i],
        ) for i in range(0, len(categories))])

    # format the layout
    fig.update_layout(
        title='Maior janela de trend para os vídeos de cada categoria',
        xaxis=dict(title='Categorias', showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(title='Tamanho da janela máxima (em dias)', zeroline=False, gridcolor='white'),
        plot_bgcolor='rgb(233,233,233)',
        width=1200,
        height=600
    )

    return fig

def display_boxplot_min_time_to_trend():
    def get_trend_start_time(df):
        return (df['trending_date'].iloc[0] - df['publish_time'].iloc[0]).days

    trend_start_time = us_data.groupby(['title', 'publish_time']).apply(get_trend_start_time)
    trend_start_time = trend_start_time.to_frame('trend_start_time')
    trend_start_time = trend_start_time.reset_index()
    trend_start_time = trend_start_time.drop('publish_time', axis=1)

    trend_start_time = trend_start_time.merge(us_data[['title', 'category_name']])
    trend_start_time = trend_start_time.drop_duplicates()

    categories = sorted(trend_start_time['category_name'].unique())
    # Each box is represented by a dict that contains the data, the type, and the colour.
    # Use list comprehension to describe N boxes, each with a different colour and with different randomly generated data:
    fig = go.Figure(data=[go.Box(
        y=trend_start_time[trend_start_time['category_name'] == categories[i]]['trend_start_time'],
        marker_color=CATEGORY_COLORS[i],
        name= categories[i],
        ) for i in range(0, len(categories))])

    # format the layout
    fig.update_layout(
        title='Tempo necessário em dias para o vídeo entrar em trend',
        xaxis=dict(title='Categorias', showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(title='Tempo necessário (em dias)', zeroline=False, gridcolor='white'),
        plot_bgcolor='rgb(233,233,233)',
        width=1200,
        height=600
    )

    return fig

layout = html.Div([
    html.H3('Análises de Tempo de Trending (Em Alta)'),
    html.P('Coloque aqui uma breve descrição da visualização, como interagir e insights.'),
    html.Div([
        html.Img(src=app.get_asset_url('trend_count.png'), style={"width": "50%"}),
        dcc.Graph(id='boxplot-trend-count', figure=display_boxplot_number_trend()),
        html.Img(src=app.get_asset_url('max_trend_window.png'), style={"width": "50%"}),
        dcc.Graph(id='boxplot-max-trend-window', figure=display_boxplot_max_trend_window()),
        html.Img(src=app.get_asset_url('trend_start_time.png'), style={"width": "50%"}),
        dcc.Graph(id='boxplot-min-time-to-trend', figure=display_boxplot_min_time_to_trend())
    ], style={"display": "flex", "flex-direction": "column", "align-items": "center"})
])

# layout = html.Div([
#     html.H3('Análises de Tempo de Trending (Em Alta)'),
#     html.P('Coloque aqui uma breve descrição da visualização, como interagir e insights.'),
#     html.Div([
#         html.Div([
#             html.Img(src=app.get_asset_url('trend_count.png'), style={"width": "45%"}),
#             html.Img(src=app.get_asset_url('max_trend_window.png'), style={"width": "45%"}),
#         ], style={"display": "flex", "justify-content": "space-around"}),
#         html.Img(src=app.get_asset_url('trend_start_time.png'), style={"width": "50%"}),
#     ],
#         style={"display": "flex", "flex-direction": "column", "align-items": "center"}
#     )
# ])