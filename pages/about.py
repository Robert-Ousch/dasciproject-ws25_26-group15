import dash
from dash import html

dash.register_page(__name__)

layout = html.Div([
    html.H1('About us', style = {'textAlign':'center'}),
    html.Div('Some text about us:'),
])
