import requests
import pandas as pd
import dash
import json
from dash import html, dcc, callback, Input, Output
import plotly.graph_objects as go
import plotly.express as px

### Calculations (Q4.py) ###
def get_matches(league, season):
    url = f"https://api.openligadb.de/getmatchdata/{league}/{season}"
    return requests.get(url).json()

all_matches = []
for season in [2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024]:
    for m in get_matches("bl1", season):
        all_matches.append({"season": season, "match": m})

records = []
for entry in all_matches:
    m = entry["match"]
    if not m.get("matchIsFinished"):
        continue
    results = m.get("matchResults", [])
    ht = next((r for r in results if r["resultTypeID"] == 1), None)
    ft = next((r for r in results if r["resultTypeID"] == 2), None)
    if not ht or not ft:
        continue
    records.append({
        "season":   entry["season"],
        "team1":    m["team1"]["teamName"],
        "team2":    m["team2"]["teamName"],
        "ht_team1": ht["pointsTeam1"], "ht_team2": ht["pointsTeam2"],
        "ft_team1": ft["pointsTeam1"], "ft_team2": ft["pointsTeam2"],
    })

df = pd.DataFrame(records)

# Comeback wins
comeback_counts = {}
for i, row in df.iterrows():
    if row["ht_team1"] < row["ht_team2"] and row["ft_team1"] > row["ft_team2"]:
        comeback_counts[row["team1"]] = comeback_counts.get(row["team1"], 0) + 1
    if row["ht_team2"] < row["ht_team1"] and row["ft_team2"] > row["ft_team1"]:
        comeback_counts[row["team2"]] = comeback_counts.get(row["team2"], 0) + 1

comeback_df = (
    pd.DataFrame.from_dict(comeback_counts, orient="index", columns=["comeback_wins"])
    .sort_values("comeback_wins", ascending=False)
    .reset_index()
    .rename(columns={"index": "team"})
)

# Comeback rate
deficit_counts = {}
for i, row in df.iterrows():
    if row["ht_team1"] < row["ht_team2"]:
        deficit_counts[row["team1"]] = deficit_counts.get(row["team1"], 0) + 1
    if row["ht_team2"] < row["ht_team1"]:
        deficit_counts[row["team2"]] = deficit_counts.get(row["team2"], 0) + 1

comeback_df["halftime_deficits"] = comeback_df["team"].map(deficit_counts).fillna(0)
comeback_df["comeback_rate_%"] = (
    (comeback_df["comeback_wins"] / comeback_df["halftime_deficits"]) * 100
).round(1)

# Slope df
slope_df = comeback_df[comeback_df["halftime_deficits"] >= 5].copy()
slope_df["rank_wins"] = slope_df["comeback_wins"].rank(ascending=False, method='first').astype(int)
slope_df["rank_rate"] = slope_df["comeback_rate_%"].rank(ascending=False, method='first').astype(int)

def classify(row):
    diff = row["rank_wins"] - row["rank_rate"]
    if diff > 1:  return "up",   "blue"
    if diff < -1: return "down", "red"
    return "same", "grey"

slope_df[["movement", "color"]] = slope_df.apply(classify, axis=1, result_type="expand")

fig_q4 = go.Figure()

for i, row in slope_df.iterrows():
    #line between the 2 ranks(wincount and comeback %)
    fig_q4.add_trace(go.Scatter(
        x=[0, 1],
        y=[row["rank_wins"], row["rank_rate"]],
        mode='lines+markers',
        line=dict(color=row["color"], width=2),
        marker=dict(size=7, color=row["color"]),
        showlegend=False,
        hovertemplate=f"{row['team']}<br>Comebackwins Rank: #{row['rank_wins']}<br>Comebackrate Rank: #{row['rank_rate']}<extra></extra>"
    ))
    #teamnames left
    fig_q4.add_annotation(x=0, y=row["rank_wins"], text=row["team"],
                          xanchor="right", showarrow=False, font=dict(size=9))
    #teamnames right
    fig_q4.add_annotation(x=1, y=row["rank_rate"], text=row["team"],
                          xanchor="left", showarrow=False, font=dict(size=9))

fig_q4.update_layout(
    xaxis=dict(
        tickvals=[0, 1],
        ticktext=["Rank by Comeback Wins", "Rank by Comeback Rate"],
        range=[-0.5, 1.5]
    ),
    yaxis=dict(autorange="reversed", title="Rank"),
    height=700,
)

### Page Layout ###
dash.register_page(__name__)

layout = html.Div([
            html.H3('Question 4: Which teams are the best at staging comebacks after trailing at half time?'),
            dcc.Graph(id='q4_static', figure=fig_q4),
            dcc.RadioItems(
                id='q4_radio',
                options=[
                        {'label': '  Comeback Wins', 'value': 'comeback_wins'},
                        {'label': '  Comeback Rate', 'value': 'comeback_rate_%'},
                ],
                value='comeback_wins',
                inline=True,
            ),
            dcc.Graph(id='q4_sort'),
        ], id='Q4Div')


### Callback ###

@callback(
    Output('q4_sort', 'figure'),
    Input('q4_radio', 'value')
)
def update_q4(sort_by):
    filtered = slope_df.sort_values(sort_by, ascending=False).head(15)
    fig = px.scatter(filtered, x=sort_by, y='team', color=sort_by,
                     color_continuous_scale=px.colors.sequential.Greens[3:],
                     title=f'Top 15 Teams sorted by {sort_by}')
    fig.update_traces(marker=dict(size=12))
    fig.update_layout(yaxis=dict(autorange='reversed'))
    return fig