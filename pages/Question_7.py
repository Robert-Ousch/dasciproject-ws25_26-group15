import requests, json
import pandas as pd
import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px


### Calculations ###
def df7():
    result = {}
    # year: goal_away per team

    alternatives = ['1. FSV Mainz 05', 'TSG 1899 Hoffenheim', 'TSG Hoffenheim', 'Bayer 04 Leverkusen', \
                'FC Bayern München', 'Borussia Dortmund', 'Borussia Mönchengladbach', \
                'VfL Wolfsburg']

    for x in range(15):
        season = 2010 + x
        result[season] = {}
        url = "https://api.openligadb.de/getmatchdata/bl1/" + str(season)
        response = requests.get(url)
        response = response.json()

        # get total number of goals away
        for match in response:
            teamName2 = match['team2']['teamName']
            if teamName2 == 'TSG 1899 Hoffenheim':
                teamName2 = 'TSG Hoffenheim'
            if teamName2 in alternatives:
                if teamName2 not in result[season].keys():
                    result[season][teamName2] = 0
            
                goals = match ['goals']
                score1 = 0
                score2 = 0        
                for goal in goals:
                    score1new = goal ['scoreTeam1'] 
                    score2new = goal ['scoreTeam2']
                    if score1new != None and score2new != None:
                        if score1new > score1:      # home goal team 1
                            score1 = score1new
                        else:       # away goal team 2
                            result[season][teamName2] += 1
                            score2 = score2new

    df = pd.DataFrame.from_dict(result)
    df = df.transpose()
    return df

df7 = df7()


### Page Layout ###
dash.register_page(__name__)

layout = html.Div([
            html.H3('Question 7: During the last 15 years (seasons 09/10 to 24/25), \
                when did each team score goals most often in their opponent`s city?'),
            html.P('When looking at the last 15 years at the seasons of 09/10 to 24/25, \
	            seven teams played in the 1st Bundesliga in each season.\
	            These teams can be selected in the dropdown below.\
	            The line chart presents the change of the amount of goals sored \
                during all away matches per season for the chosen team(s).'),
            html.P("Select one or more teams to compare:"),
            dcc.Dropdown(
                options = ['1. FSV Mainz 05', 'TSG Hoffenheim', 'Bayer 04 Leverkusen', \
                    'FC Bayern München', 'Borussia Dortmund', 'Borussia Mönchengladbach', \
                    'VfL Wolfsburg'], 
                value = ['FC Bayern München'], 
                multi = True,  
                id = 'component7'),
            html.Div(dcc.Graph(id = 'graph7')),
        ], id = 'Q7Div'),


### Callback ###
@callback(
    Output(component_id = 'graph7', component_property = 'figure'),
    Input(component_id = 'component7', component_property = 'value')
)
def upgrade_graph_7(value_chosen):
    fig7 = px.line(df7, y = value_chosen)
    fig7.update_layout(
        xaxis_title = 'Year', 
        yaxis_title = 'Total number of goals'
    )
    return fig7