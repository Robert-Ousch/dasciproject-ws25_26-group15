import pandas as pd
import requests
import json
import dash
from dash import html, dcc, callback, Input, Output
import plotly.graph_objects as go


### Calculations ###
def df_6():
    '''
    This function uses the openligadb API to extract the teams playing in the season
    range as well as the total number of goals scored per season.
    i: none
    o: DataFrame
    '''
    result = {}
    for x in range(15):
        # access the match data
        season = 2010 + x
        response = requests.get('https://api.openligadb.de/getmatchdata/bl1/' + \
            str(season))
        response = response.json()

        for match in response:
            # get home team, if new add as key to result
            team_name_1 = match['team1']['teamName']
            if team_name_1 not in result.keys():
                result[team_name_1] = {}
            if season not in result[team_name_1].keys():
                result[team_name_1][season] = 0

            # get all goals in match for the home team
            goals = match['goals']
            score_1 = 0
            score_2 = 0
            for goal in goals:
                score_1_new = goal['scoreTeam1'] 
                score_2_new = goal['scoreTeam2']
                if score_1_new != None and score_2_new != None:
                    if score_1_new > score_1:       # home goal 
                        result[team_name_1][season] += 1
                        score_1 = score_1_new
                    else:       
                        score_2 = score_2_new
    df = pd.DataFrame.from_dict(result)
    df = df.transpose()
    return df


df6 = df_6()


def plot_category_lollipop(grouped_df, category_key, value_key):
    '''
    This function constructs a lollipop graph for the given dataframe and keys
    i: DataFrame and two keys
    o: lollipop graph
    '''
    grouped_df = grouped_df.sort_values(by = value_key)
    fig_data = []
    
    # plot the lines
    fig_data.extend([
        go.Scatter(
            x = [0, count],
            y = [category, category],
            mode = "lines",
            line = dict(color = "silver", width = 3),
            showlegend = False
        )
        for category, count in zip(grouped_df[category_key], grouped_df[value_key])   
    ])

    # plot the dots and the text
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


layout = html.Div([
    html.H3('Question 6: Which teams scored goals at home turf most often?'),
    html.P('This question provides an overview for one season at a time, which can be\
        chosen using the slider below between the seasons 2010 and 2024.\
        The lollipop graph displays all teams, that played in the chosen season, \
        as well as the number of goals each team scored during all home matches \
        of the chosen season.'),
    html.P('Select the year to consider:'),
    dcc.Slider(2010, 2024, 1, value = 2010, id = 'component6'),
    html.Div(dcc.Graph(id = 'graph6')), 
], id = 'Q6Div')


### Callback ###
@callback(
    Output(component_id = 'graph6', component_property = 'figure'),
    Input(component_id = 'component6', component_property = 'value')
)


def upgrade_graph_6(value_chosen):
    '''
    This function computes the lollipop graph for the chosen year.
    i: year
    o: updated graph
    '''
    dict = pd.DataFrame.to_dict(df6)        # convert df to dict
    dict = dict[value_chosen]
    dict_new = {}       # create new dict with correct labels
    for key in dict.keys():
        if dict[key] >= 0:  
            dict_new[key] = {'team': key, 'goals': dict[key]}
    df_new = pd.DataFrame.from_dict(dict_new).transpose()      # convert dict to df
    fig = plot_category_lollipop(df_new, category_key = 'team', value_key = 'goals')
    return fig