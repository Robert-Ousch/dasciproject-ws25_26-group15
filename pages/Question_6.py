import requests, json
import pandas as pd
import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go


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

def plot_category_lollipop(grouped_df, category_key, value_key):
    ''' source:
    https://hi-artemii.medium.com/vertical-lollipop-chart-in-\
    plotly-python-minimal-code-example-1e1bca0b1261
    '''
    grouped_df = grouped_df.sort_values(by=value_key)
    fig_data = []
    fig_data.extend([
        go.Scatter(
            x = [0, count],
            y = [category, category],
            mode = "lines",
            line = dict(color="silver", width=3),
            showlegend = False
        )
        for category, count in zip(grouped_df[category_key], grouped_df[value_key])   
    ])
    fig_data.append(
        go.Scatter(
            x = grouped_df[value_key],
            y = grouped_df[category_key],
            mode = "markers+text",
            marker = dict(color = "DarkBlue", size = 16.0),
            text = [f"{x}" for x in grouped_df[value_key]],
            textposition = "middle right",
            showlegend = False
        )
    )
    fig = go.Figure(fig_data)
    fig.update_yaxes(dtick = 1)
    return fig



### Page Layout ###
dash.register_page(__name__)

layout = html.Div(
    [
        html.H3('Question 6: Which teams scored goals at home turf most often?'),
        html.P('This question provides an overview for one season at a time, which can be\
            chosen using the slider below between the seasons 2010 and 2024.\
            The lollipop graph displays all teams, that played in the chosen season, \
            as well as the number of goals each team scored during all home matches \
            of the chosen season'),
        html.P('Select the year to consider:'),
        dcc.Slider(2010, 2024, 1, value=2010, id='component6'),
        html.Div(dcc.Graph(id = 'graph6')), 
    ], id = 'Q6Div')


### Callback ###
@callback(
    Output(component_id = 'graph6', component_property = 'figure'),
    Input(component_id = 'component6', component_property = 'value')
)
def upgrade_graph_6(value_chosen):
    dict6 = pd.DataFrame.to_dict(df6)       # convert df to dict
    dict6 = dict6[value_chosen]
    dict6_new = {}      # create new dict with correct labels
    for key in dict6.keys():
        if dict6[key] >= 0:  
            dict6_new[key] = {'team': key, 'goals': dict6[key]}
    df6_new = pd.DataFrame.from_dict(dict6_new).transpose()     # convert dict to df
    fig6 = plot_category_lollipop(df6_new, category_key = 'team', value_key = 'goals')
    return fig6