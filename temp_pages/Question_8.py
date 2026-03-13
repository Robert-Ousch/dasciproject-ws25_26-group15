import requests, json
import pandas as pd
import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px


### Calculations ###


### Page Layout ###
dash.register_page(__name__)

layout = html.Div([
            html.H3('Question 8: How does the venue capacity influence the win rate of the \
                away team for the seasons 2022-2024?'),
            dcc.RangeSlider(10000, 100000, 1000, value=[10000, 100000], id = 'component8_1'),
            dcc.Dropdown(
                options = ['1. FC Heidenheim 1846', '1. FC Köln', '1. FC Union Berlin', '1. FSV Mainz 05', \
                    'Bayer 04 Leverkusen', 'Borussia Dortmund', 'Borussia Mönchengladbach', \
                    'Eintracht Frankfurt', 'FC Augsburg', 'FC Bayern München', 'FC Schalke 04', 'FC St. Pauli', \
                    'Hertha BSC', 'RB Leipzig', 'SC Freiburg', 'SV Darmstadt 98', 'SV Werder Bremen', \
                    'TSG Hoffenheim', 'VfB Stuttgart', 'VfL Bochum', 'VfL Wolfsburg'], 
                value = ['FC Bayern München'],
                multi = True, 
                id = 'component8_2'),
            html.Div(dcc.Graph(id = 'graph8', figure = px.scatter(df8))) 
        ], id = 'Q8Div')

### Callback ###
@callback(
    Output(component_id = 'graph8', component_property = 'figure'),
    Input(component_id = 'component8_1', component_property = 'value'),
    Input(component_id = 'component8_2', component_property = 'value')
)
def upgrade_graph_8(slider, value_chosen): 
    df_temp = pd.DataFrame({})
    rows = df8.loc[(df8.index >= slider[0]) & (df8.index <= slider[1])]
    df_temp = pd.concat([df_temp, rows])
    return px.scatter(df_temp, y = value_chosen)