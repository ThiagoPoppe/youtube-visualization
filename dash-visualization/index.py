import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from apps import formato_metricas, sumario_metricas, trend_categoria, pequenos_multiplos, metricas_periodo


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Trend Categoria|', href='/trend_categoria'),
        dcc.Link('Formato das Métricas|', href='/formato_metricas'),
        dcc.Link('Sumário das Métricas|', href='/sumario_metricas'),
        dcc.Link('Pequenos Múltiplos|', href='/pequenos_multiplos'),
        dcc.Link('Métricas por período|', href='/metricas_periodo'),
    ], className="row"),
    html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/trend_categoria':
        return trend_categoria.layout
    if pathname == '/formato_metricas':
        return formato_metricas.layout
    if pathname == '/sumario_metricas':
        return sumario_metricas.layout
    if pathname == '/pequenos_multiplos':
        return pequenos_multiplos.layout
    if pathname == '/metricas_periodo':
        return metricas_periodo.layout
    else:
        return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=False)