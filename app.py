import dash
from dash import Dash, html, dcc
import os

app = Dash(__name__, use_pages=True)
server = app.server

app.layout = html.Div([
    html.H1('Data Science Project WS 25/26', style = {'textAlign':'centering'}),
    html.Div([
        html.Div(
            dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
    dash.page_container
])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5002))
    app.run(debug=True, use_reloader = False, host = '0.0.0.0', port = port)