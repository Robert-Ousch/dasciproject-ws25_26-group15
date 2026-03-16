import requests, json
import pandas as pd
import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px


### Calculations ###
with open("data_Q8.txt", "r") as file:
    data_Q8 = json.loads(file.read())
df8 = pd.DataFrame(data_Q8)
df8 = df8.sort_index()
#df8.index = df8.index.astype(int)

### Page Layout ###
dash.register_page(__name__)

layout = html.Div([
            html.H3('Question 8: How does the venue capacity influence the win rate of the \
                away team for the seasons 2022-2024?'),
            html.P("Select upper and lower bounds for the venue capacity:"),
            dcc.Checklist(
                options = ['15000', '17810', '22467', '27599', '29564', '30000', '30164', '30210', '30662', \
                '34034', '34700', '42358', '47069', '50076', '54057', '58000', '60469', '62278', '74667', \
                '75024', '81365'],
                value = ['15000', '17810', '22467', '27599', '29564', '30000', '30164', '30210', '30662', \
                '34034', '34700', '42358', '47069', '50076', '54057', '58000', '60469', '62278', '74667', \
                '75024', '81365'],
                inline = True,
                id = 'component8_1'),
            html.P("Select one or more teams to compare:"),
            dcc.Dropdown(
                options = ['1. FC Heidenheim 1846', '1. FC Köln',	'1. FC Union Berlin', '1. FSV Mainz 05', \
                    'Bayer 04 Leverkusen', 'Borussia Dortmund', 'Borussia Mönchengladbach', \
                    'Eintracht Frankfurt', 'FC Augsburg', 'FC Bayern München', 'FC Schalke 04', 'FC St. Pauli', \
                    'Hertha BSC', 'RB Leipzig', 'SC Freiburg', 'SV Darmstadt 98', 'SV Werder Bremen', \
                    'TSG Hoffenheim', 'VfB Stuttgart', 'VfL Bochum', 'VfL Wolfsburg'], 
                value = ['FC Bayern München'],
                multi = True,
                id = 'component8_2'),
            html.Div(dcc.Graph(id = 'graph8', figure = px.imshow(df8))) 
        ], id = 'Q8Div')

### Callback ###
@callback(
    Output(component_id = 'graph8', component_property = 'figure'),
    #Input(component_id = 'component8_1', component_property = 'value'),
    Input(component_id = 'component8_2', component_property = 'value')
)
def upgrade_graph_8(team_chosen):
    fig8 = px.imshow(df8[team_chosen])
    fig8.update_xaxes(nticks = len(team_chosen))
    return fig8 
''' 
def upgrade_graph_8(capacity_chosen, team_chosen):
    df_temp = pd.DataFrame({})
    #rows = df8.loc[(df8.index >= slider[0]) & (df8.index <= slider[1])]
    rows = df8.loc[(capacity_chosen in df8.index)]
    df_temp = pd.concat([df_temp, rows]) 
    fig8 = px.imshow(df8[team_chosen])
    fig8.update_xaxes(nticks = len(team_chosen))
    return fig8 
'''