import dash
from dash import Dash, html, dcc
import os

e_s = [
    'https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap'
]

app = Dash(__name__, use_pages=True, external_stylesheets=e_s)
server = app.server

nav_style = {
    'display': 'flex', 'gap': '8px', 'padding': '12px 0', 'borderBottom': '1px solid #ddd'
}

link_style = {
    'padding': '6px 14px', 'border': '1px solid #ccc', 'borderRadius': '4px',
    'textDecoration': 'none', 'color': '#333', 'fontSize': '14px'
}



app.layout = html.Div([
    html.H1('Data Science Project WS 25/26', style={'textAlign': 'center'}),
    html.Div([
        dcc.Link(page['name'], href=page["relative_path"], style=link_style)
        for page in dash.page_registry.values()
    ], style=nav_style),
    dash.page_container
], style={'padding': '0 12%'})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    app.run(debug=True, use_reloader = False, host = '0.0.0.0', port = port)