import dash_html_components as html

from app import app

layout = html.Div([
    html.H3('Pequenos Múltiplos'),
    html.Div([
        html.Div([
            html.Img(src=app.get_asset_url('max_trend_window.png'), style={"width": "45%"}),
            html.Img(src=app.get_asset_url('trend_count.png'), style={"width": "45%"}),
        ], style={"display": "flex", "justify-content": "space-around"}),
        html.Img(src=app.get_asset_url('trend_start_time.png'), style={"width": "50%"}),
    ],
        style={"display": "flex", "flex-direction": "column", "align-items": "center"}
    )
])