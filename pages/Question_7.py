import requests
import json
import pandas as pd
import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px


### Calculations ###
def df_7():
    '''
    This function uses the openligadb API to extract the teams playing in the season
    range as well as the total number of goals scored per season.
    i: none
    o: DataFrame
    '''
    result = {}
    alternatives = ['1. FSV Mainz 05', 'TSG 1899 Hoffenheim', 'TSG Hoffenheim', \
        'Bayer 04 Leverkusen', 'FC Bayern München', 'Borussia Dortmund', \
        'Borussia Mönchengladbach', 'VfL Wolfsburg']
    for x in range(15):
        # access the match data
        season = 2010 + x
        result[season] = {}
        url = 'https://api.openligadb.de/getmatchdata/bl1/'+ str(season)
        response = requests.get(url)
        response = response.json()

        for match in response:
            # get away team, if new add as key to result
            team_name_2 = match['team2']['teamName']
            if team_name_2 == 'TSG 1899 Hoffenheim':
                team_name_2 = 'TSG Hoffenheim'
            if team_name_2 in alternatives:
                if team_name_2 not in result[season].keys():
                    result[season][team_name_2] = 0
                
                # get all goals in match for the away team
                goals = match['goals']
                score_1 = 0
                score_2 = 0        
                for goal in goals:
                    score_1_new = goal['scoreTeam1'] 
                    score_2_new = goal['scoreTeam2']
                    if score_1_new != None and score_2_new != None:
                        if score_1_new > score_1:      
                            score_1 = score_1_new
                        else:       # away goal 
                            result[season][team_name_2] += 1
                            score_2 = score_2_new
    df = pd.DataFrame.from_dict(result)
    df = df.transpose()
    return df


df7 = df_7()


### Page Layout ###
dash.register_page(__name__)


layout = html.Div([
    html.H3('Question 7: During the last 15 years, \
        when did each team score goals most often in their opponent`s city?'),
    html.P('When looking at the seasons of 09/10 to 24/25, \
	    seven teams played in the 1st Bundesliga in each season.\
	    These teams can be selected in the dropdown below.\
	    The line chart presents the change of the amount of goals sored \
        during all away matches per season for the chosen team(s).'),
    html.P('Select one or more teams to compare:'),
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
    '''
    This function computes the line graph for the chosen teams.
    i: array of teams
    o: updated graph
    '''
    fig = px.line(df7, y = value_chosen, color_discrete_sequence = ["#6175c4",\
        "#cf47a3","#58a9d7","#8a5dcf","#d878a3","#cb8cda","#954b85"])
    fig.update_layout(
        xaxis_title = 'Year', 
        yaxis_title = 'Total number of goals'
    )
    fig.update_xaxes(nticks = 15, tickangle = 45)
    return fig