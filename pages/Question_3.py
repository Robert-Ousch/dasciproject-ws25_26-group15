import requests, json
import pandas as pd
import dash
import statistics
from dash import html, dcc, callback, Input, Output
import plotly.express as px

### Page Layout ###
dash.register_page(__name__)


with open("./.data_Q3.txt", "r") as file:
    data_Q3 = json.loads(file.read())

df3_r = pd.DataFrame()
df3_p = pd.DataFrame()
avgs_r = []
precs_r = []
avgs_p = []
precs_p = []
for i in range(0, 350):
    matches_r = list(filter(lambda x: i/10 <= x[1] < i/10+0.1, list(zip(data_Q3["Goals"], data_Q3["Rain"], data_Q3["Precipitation"]))))
    matches_p = list(filter(lambda x: i/10 <= x[2] < i/10+0.1, list(zip(data_Q3["Goals"], data_Q3["Rain"], data_Q3["Precipitation"]))))
    if len(matches_r) > 5:
        avgs_r.append(statistics.mean([x for (x, _, _) in matches_r]))
        precs_r.append(i/10)
    if len(matches_p) > 5:
        avgs_p.append(statistics.mean([x for (x, _, _) in matches_p]))
        precs_p.append(i/10)

df3_r["Average goals per match"] = avgs_r
df3_r["Precipitation group"] = precs_r
fig_Q3_r = px.scatter(df3_r, x="Precipitation group",y="Average goals per match", trendline="ols")
df3_p["Average goals per match"] = avgs_p
df3_p["Rain group"] = precs_p
fig_Q3_p = px.scatter(df3_p, x="Rain group",y="Average goals per match", trendline="ols")

layout = html.Div([
            html.H3('[Question 3]'),
            html.Div(dcc.RadioItems(["Rain", "Precipitation"], "Rain", id="Q3_rain_select")),
            html.Div(children=dcc.Graph(id= "Q3_1", figure=px.scatter())),
        ], id = 'Q3Div'),


@callback(
        Output(component_id="Q3_1", component_property="figure"),
        Input(component_id="Q3_rain_select", component_property="value")
)
def Q3_graph_switch(selection):
    if selection=="Rain":
        return fig_Q3_r
    else:
        return fig_Q3_p
