import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import (
    initial_page, visao_geral, formato_metricas, ranking_das_metricas,
    sumario_metricas, tempo_de_trending, metricas_periodo
)

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "2rem 1rem",
    "background-color": "#212121",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "20rem",
    "text-align": "center",
}

sidebar = html.Div(
    [
        html.H1("YouTube Trending Data", className="display-4", style={"color": "white"}),
        html.Hr(),
        html.P(
            "Selecione uma página para visualizar os dados", className="lead",
            style={"color": "white"}
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Visão Geral", href="/visao_geral", active="exact"),
                dbc.NavLink("Ranking das Métricas", href="/ranking_das_metricas", active="exact"),
                dbc.NavLink("Formato das Métricas", href="/formato_metricas", active="exact"),
                dbc.NavLink("Sumário das Métricas", href="/sumario_metricas", active="exact"),
                dbc.NavLink("Métricas por período", href="/metricas_periodo", active="exact"),
                dbc.NavLink("Tempo de Trending", href="/tempo_de_trending", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

footer = html.Footer([
        'Esse projeto foi desenvolvido pelos alunos: Giovanna Louzi Bellonia, João Vítor Campos Teixeira, Larissa Gomes Malagoli e Thiago Martin Poppe.'
])

app.layout = html.Div([dcc.Location(id="url"), sidebar, content, footer])

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/':
        return initial_page.layout
    
    if pathname == '/visao_geral':
        return visao_geral.layout

    if pathname == '/ranking_das_metricas':
        return ranking_das_metricas.layout
    
    if pathname == '/formato_metricas':
        return formato_metricas.layout
    
    if pathname == '/sumario_metricas':
        return sumario_metricas.layout
    
    if pathname == '/metricas_periodo':
        return metricas_periodo.layout

    if pathname == '/tempo_de_trending':
        return tempo_de_trending.layout

    # If the user tries to reach a different page, return a 404 message
    else:
        return dbc.Jumbotron(
            [
                html.H1(
                    "404: Not found",
                    style={"textAlign": "center"},
                    className="text-danger"
                ),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ]
        )
        
if __name__ == '__main__':
    app.run_server(debug=True)