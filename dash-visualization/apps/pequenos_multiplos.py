import dash_html_components as html
from app import app

    
layout = html.Div([
    html.H1('Pequenos Múltiplos', style={"textAlign": "center"}),
    html.Div([
        html.Img(src=app.get_asset_url('max_trend_window.png'), style={"width": "35%"}),
        html.Img(src=app.get_asset_url('trend_count.png'), style={"width": "35%"}),
        html.Img(src=app.get_asset_url('trend_start_time.png'), style={"width": "35%"}),
    ],
        style={"display": "flex", "flex-direction": "column", "align-items": "center"}
    )
])