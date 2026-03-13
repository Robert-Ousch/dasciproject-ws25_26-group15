import requests, json
import pandas as pd
import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px


### Calculations ###
def df6():
    result = {}
    # teamName: goals_home per season

    for x in range(15):
        season = 2010 + x
        response = requests.get("https://api.openligadb.de/getmatchdata/bl1/" + str(season))
        response = response.json()

        for match in response:
            # get both teams, if new add as keys to result
            teamName1 = match['team1']['teamName']
            teamName2 = match['team2']['teamName']
            if teamName1 not in result.keys():
                result[teamName1] = {}
            if teamName2 not in result.keys():
                result[teamName2] = {}
            if season not in result[teamName1].keys():
                result[teamName1][season] = 0
            if season not in result[teamName2].keys():
                result[teamName2][season] = 0
        
            # get all goals in match and team that scored them 
            goals = match['goals']
            score1 = 0
            score2 = 0
            for goal in goals:
                score1new = goal['scoreTeam1'] 
                score2new = goal['scoreTeam2']
                if score1new != None and score2new != None:
                    if score1new > score1:      # home goal team 1
                        result[teamName1][season] += 1
                        score1 = score1new
                    else:       # away goal team 2
                        score2 = score2new

    df = pd.DataFrame.from_dict(result)
    df = df.transpose()
    return df

df6 = df6()


### Page Layout ###
dash.register_page(__name__)

layout = html.Div([
            html.H3('Question 6: Which teams scored goals at home turf most often?'),
            html.P("Select the year to consider:"),
            dcc.Slider(2010, 2024, 1, value=2010, id='component6'),
            html.Div(dcc.Graph(id = 'graph6')), 
        ], id = 'Q6Div'),


### Callback ###
@callback(
    Output(component_id = 'graph6', component_property = 'figure'),
    Input(component_id = 'component6', component_property = 'value')
)
def upgrade_graph_6(value_chosen):
    fig6 = px.bar(df6, y = value_chosen)
    fig6.update_layout(
        xaxis_title = 'Team Names', 
        yaxis_title = 'Total number of goals'
    )
    return fig6