import statistics
import json
import pandas as pd
import dash

from dash import html, dcc, callback, Input, Output
import plotly.express as px

### Page Layout ###
dash.register_page(__name__)


with open("./.data_Q3.txt", "r") as file:
    # structured like {"goals": [goals match 1, ...], "rain":
    # [rain match 1, ...], "precipitation: [precipitation match 1, ...]"}
    data_Q3 = json.loads(file.read())

df3_r = pd.DataFrame()
df3_p = pd.DataFrame()
# average goals, precipitation/rain amounts, and sample sizes for each bucket
avgs_r = []
precs_r = []
ss_r = []
avgs_p = []
precs_p = []
ss_p = []
for i in range(350):
    # create and analyze the buckets
    matches_r = list(filter(lambda x: i/10 <= x[1] < i/10 + 0.1,
        list(zip(data_Q3["Goals"], data_Q3["Rain"],
            data_Q3["Precipitation"]))))
    matches_p = list(filter(lambda x: i/10 <= x[2] < i/10 + 0.1,
        list(zip(data_Q3["Goals"], data_Q3["Rain"],
            data_Q3["Precipitation"]))))
    if len(matches_r) > 5:
        avgs_r.append(statistics.mean([x for (x, _, _) in matches_r]))
        precs_r.append(i/10)
        ss_r.append(len(matches_r))
    if len(matches_p) > 5:
        avgs_p.append(statistics.mean([x for (x, _, _) in matches_p]))
        precs_p.append(i/10)
        ss_p.append(len(matches_p))

df3_r["Average goals per match"] = avgs_r
df3_r["Rain in mm"] = precs_r
df3_r["Sample size"] = ss_r
fig_Q3_r = px.scatter(df3_r, x="Rain in mm", y="Average goals per match",
    trendline="ols", hover_data="Sample size")
df3_p["Average goals per match"] = avgs_p
df3_p["Precipitation in mm"] = precs_p
df3_p["Sample size"] = ss_p
fig_Q3_p = px.scatter(df3_p, x="Precipitation in mm",
    y="Average goals per match",
    trendline="ols",
    hover_data="Sample size")

layout = [
    html.Div([
        html.H3("Question 3: How does high precipitation during a match " \
                "influence the total number of goals scored?"),
        html.P("Taking a step back from the previous question, on this page" \
        " we're interested in a general trend in the amount of goals scored" \
        " during the average football match as the precipitation changes." \
        " We therefore group matches into buckets based on precipitation " \
        "with a bucket size of 0.1mm, then plot the average number of goals" \
        " for each bucket below. This naturally creates an imbalance in the" \
        " bucket sizes, as about half of all games see no precipitation at " \
        "all whereas only about a quarter of games see a precipitation " \
        "greater than 3mm. This is the reason for the increase in variance" \
        " we observe in the plot, not the precipitation itself. Only buckets"\
        " with a size of 6 or greater are considered to eliminate outliers. "\
        "As we can see, the observed trend varies little when considering " \
        "rain specifically as opposed to precipitation, which also includes" \
        " all other ways water can fall from the sky."),
        html.Div(dcc.RadioItems(["Rain", "Precipitation"], "Precipitation",
            id="Q3_rain_select")),
        html.Div(children=dcc.Graph(id= "Q3_1", figure=px.scatter())),
    ], id = 'Q3Div')
    ]


@callback(
        Output(component_id="Q3_1", component_property="figure"),
        Input(component_id="Q3_rain_select", component_property="value")
)
def q3_graph_switch(selection):
    '''callback to allow the user to toggle between the graphs'''
    if selection=="Rain":
        return fig_Q3_r
    return fig_Q3_p
