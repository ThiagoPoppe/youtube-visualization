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
trend_count = us_data.groupby(['title', 'category_name']).size()
trend_count = trend_count.reset_index(name='trend_count')

def display_fig():
    N = 30     # Number of boxes

    # generate an array of rainbow colors by fixing the saturation and lightness of the HSL
    # representation of colour and marching around the hue.
    # Plotly accepts any CSS color format, see e.g. http://www.w3schools.com/cssref/css_colors_legal.asp.
    c = ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 360, N)]

    categories = trend_count['category_name'].unique()
    # Each box is represented by a dict that contains the data, the type, and the colour.
    # Use list comprehension to describe N boxes, each with a different colour and with different randomly generated data:
    fig = go.Figure(data=[go.Box(
        y=trend_count[trend_count['category_name'] == categories[i]]['trend_count'],
        marker_color=c[i],
        name= categories[i],
        ) for i in range(0, len(categories))])

    # format the layout
    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(zeroline=False, gridcolor='white'),
        paper_bgcolor='rgb(233,233,233)',
        plot_bgcolor='rgb(233,233,233)',
    )

    # fig.show()
    return fig
    
layout = html.Div([
    html.H1('Trend Category', style={"textAlign": "center"}),
    dcc.Graph(id='my-graph', figure=display_fig()),
])