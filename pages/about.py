import dash
from dash import html

dash.register_page(__name__)

layout = html.Div([
    html.H1('About us', style = {'textAlign':'center'}),
    html.P('This project is created as part of the Data Science Project of the '\
        'winter semester 2025/26 from Cristian-Albrechts-University in Kiel. '\
        'Our group is number 15 and the team members are Hauke Busch, Jakob Erichsen, '\
        'Alexander Liebler and Robert Ousch.')
])
