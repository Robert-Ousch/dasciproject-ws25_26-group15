import requests, json
import pandas as pd
import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px

### Page Layout ###
dash.register_page(__name__)

with open("./.data_Q2.txt", "r") as file:
    data_Q2 = json.loads(file.read())

diagrams = []

def filter_prec(data, threshold):
    teams_lt = []
    goals_lt = []
    teams_gt = []
    goals_gt =[]
    df1 = pd.DataFrame()
    df2 = pd.DataFrame()
    counts_lt = {}
    counts_gt = {}
    for team, matches in data.items():
        for match in list(zip(*matches)):
            if match[1] > threshold:
                if team in counts_gt:
                    counts_gt[team] += 1
                else:
                    counts_gt[team] = 1
                teams_gt.append(team)
                goals_gt.append(match[0])
            else:
                if team in counts_lt:
                    counts_lt[team] += 1
                else:
                    counts_lt[team] = 1
                teams_lt.append(team)
                goals_lt.append(match[0])
    teams_lt = [team + " (" + str(counts_lt[team]) + ")" for team in teams_lt]
    teams_gt = [team + " (" + str(counts_gt[team]) + ")" for team in teams_gt]
    df1["Teams (# Matches)"] = teams_lt
    df1["Goals"] = goals_lt
    df2["Teams (# Matches)"] = teams_gt
    df2["Goals"] = goals_gt
    return (px.box(df1, x="Teams (# Matches)", y="Goals", title=f"Goals distribution during games with at most {threshold}mm of precipitation"), 
            px.box(df2, x="Teams (# Matches)", y="Goals", title=f"Goals distribution during games with more than {threshold}mm of precipitation"))

layout = html.Div([
            html.H3('Question 2: How does high rainfall during a match influence the performance of certain German teams?'),
            html.P("Many football arenas in Germany do not (yet) have a roof, exposing teams and spectators alike to the elements. " \
            "We wanted to know if there are any teams out there which are particularly impacted by unfavorable weather conditions. " \
            "For this purpose, we're identifying a team's performance with the number of goals they scored during the match."),
            html.P("On this page, you will be able to answer this question for yourself. Move the slider below to see a distribution of scored " \
            "goals for all selected teams, which only takes into account matches with at most (top plot) or more than (bottom plot) " \
            "that much precipitation on the day of the match."),
            html.Div(
                [html.P("Precipitation threshold (mm):"),
                dcc.Slider(
                    id='Q2_rain_filter',
                    min=0,
                    max=35,
                    step=0.1,
                    value=1.5,
                )]
            ),
            html.Div(
                [html.P("Selected teams:"),
                dcc.Dropdown(list(data_Q2.keys()), list(data_Q2.keys()), True, True, True, id="Q2_teams_filter")]
            ),
            html.Div(children=dcc.Graph(id= "Q2_0", figure=px.bar())),
            html.Div(children=dcc.Graph(id= "Q2_1", figure=px.bar())),
        ], id = 'Q2Div')

@callback(
    Output(component_id="Q2_0", component_property="figure"),
    Output(component_id="Q2_1", component_property="figure"),
    Input(component_id="Q2_rain_filter", component_property="value"),
    Input(component_id="Q2_teams_filter", component_property="value")
)
def update_plots_Q2(threshold, selection):
    data = dict(filter(lambda x: x[0] in selection, data_Q2.items()))
    return filter_prec(data, threshold)