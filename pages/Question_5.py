import requests
import json
import pandas as pd
import dash
from dash import html, dcc, callback, Input, Output
import plotly.graph_objects as go

### Calculations (Q5.py) ###
#Load all matches from the API
def get_matches(league, season):
    url = f'https://api.openligadb.de/getmatchdata/{league}/{season}'
    return requests.get(url).json()

#load all seasons
all_matches = []
seasons = [2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]

for season in seasons:
    matches = get_matches('bl1', season)
    all_matches.extend(matches)

#extract the minute of the first lead-giving goal and the match outcome
records = []

for m in all_matches:

    
    if not m.get('matchIsFinished'):
        continue

    #get final result
    results = m.get('matchResults', [])
    ft = None
    for r in results:
        if r['resultTypeID'] == 2:
            ft = r
    if ft is None:
        continue

    #skip matches without goals
    goals = m.get('goals', [])
    if not goals:
        continue

    #final score
    ft1 = ft['pointsTeam1']
    ft2 = ft['pointsTeam2']

    #sort goals by minute
    sorted_goals = sorted(goals, key=lambda x: x.get('matchMinute') or 999)

    #track the running score
    score1 = 0
    score2 = 0

    #ttrack the first minute each team falls behind
    first_against_team1 = None
    first_against_team2 = None

    for g in sorted_goals:
        minute = g.get('matchMinute')
        if not minute or minute <= 0 or minute > 90:
            continue

        new_s1 = g.get('scoreTeam1', score1)
        new_s2 = g.get('scoreTeam2', score2)

        #Check if team 2 just took the lead for the first time
        if new_s2 > score2 and new_s2 > new_s1 and first_against_team1 is None:
            first_against_team1 = minute

        #vice versa with team 1
        if new_s1 > score1 and new_s1 > new_s2 and first_against_team2 is None:
            first_against_team2 = minute

        score1 = new_s1
        score2 = new_s2

    #save the result
    if first_against_team1 is not None:
        if ft1 < ft2:
            outcome = 'loss'
        elif ft1 == ft2:
            outcome = 'draw'
        else:
            outcome = 'win'
        records.append({'minute': first_against_team1, 'outcome': outcome})

    
    if first_against_team2 is not None:
        if ft2 < ft1:
            outcome = 'loss'
        elif ft1 == ft2:
            outcome = 'draw'
        else:
            outcome = 'win'
        records.append({'minute': first_against_team2, 'outcome': outcome})


df_q5 = pd.DataFrame(records)

#assign each minute to a 15-minute time bin
labels_q5 = ['1-15', '16-30', '31-45', '46-60', '61-75', '76-90']
df_q5['time_bin'] = pd.cut(df_q5['minute'], bins=[0, 15, 30, 45, 60, 75, 90], labels=labels_q5)

#how often each outcome occurs per time bin
outcome_dist_q5 = df_q5.groupby(['time_bin', 'outcome'], observed=True).size().unstack(fill_value=0)
outcome_dist_q5 = outcome_dist_q5.reindex(columns=['win', 'draw', 'loss'], fill_value=0)

# Convert to percentages
outcome_pct_q5 = outcome_dist_q5.div(outcome_dist_q5.sum(axis=1), axis=0) * 100

### Static Stacked Bar chart

x = outcome_pct_q5.index.astype(str)

graph = go.Figure()

graph.add_bar(
    x=x,
    y=outcome_pct_q5['win'],
    name='Win',
    marker_color='green',
    text=[f'{v:.0f}%' for v in outcome_pct_q5['win']],   
    textposition='inside'
)

graph.add_bar(
    x=x,
    y=outcome_pct_q5['draw'],
    name='Draw',
    marker_color='grey',
    text=[f'{v:.0f}%' for v in outcome_pct_q5['draw']],  # ← hinzufügen
    textposition='inside'
)

graph.add_bar(
    x=x,
    y=outcome_pct_q5['loss'],
    name='Loss',
    marker_color='red',
    text=[f'{v:.0f}%' for v in outcome_pct_q5['loss']],
    textposition='inside',
)

graph.update_layout(
    barmode='stack',
    title='Match Outcome Distribution by Timing of First Lead-Giving Goal<br>Bundesliga 2009–2024',
    xaxis_title='Minute of First Lead-Giving Goal Conceded',
    yaxis_title='Share of Matches (%)',
    yaxis=dict(range=[0,105]),
    template='plotly_white'
)

### Page Layout ###
dash.register_page(__name__)

layout = html.Div([
    html.H3('Question 5: How does the timing of the first conceded lead-giving goal affect the match outcome?'), 
    html.P('The timing of the first lead-giving goal conceded may strongly influence how a match develops. ' \
    'Conceding early still leaves time to recover, while conceding late often makes it difficult to change the outcome. ' \
    'By analyzing match results across different time intervals, we can explore how the timing of falling behind affects ' \
    'the chances of winning, drawing, or losing.  The visualizations help reveal these patterns and highlight potential differences across match situations.'),
    dcc.Graph(
        id='q5_outcome_focus',
        figure=graph
    ),
    dcc.RadioItems(
        id='q5_outcome_filter',
        options=[
            {'label': '  Win',  'value': 'win'},
            {'label': '  Draw', 'value': 'draw'},
            {'label': '  Loss', 'value': 'loss'},
        ],
        value='loss',
        inline=True,
        style={'marginBottom': '10px'}
    ),
    dcc.Graph(id='q5_outcome_focus'),
], id = 'Q5Div')

### Callback ###
@callback(
    Output('q5_outcome_focus', 'figure'),
    Input('q5_outcome_filter', 'value')
)
def update_q5_outcome(selected_outcome):
    color_map = {'win': 'green', 'draw': 'grey', 'loss': 'red'}
    x = outcome_pct_q5.index.astype(str).tolist()
    y = outcome_pct_q5[selected_outcome]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=x,
        y=y,
        marker_color=color_map[selected_outcome],
        name=selected_outcome.capitalize()
    ))
    fig.update_layout(
        title=f'Share of "{selected_outcome.capitalize()}" by Time Bins Bundesliga 2009-2024',
        xaxis_title='Minute of First Lead-Giving Goal Conceded',
        yaxis_title='Share of Matches (%)',
        yaxis=dict(range=[0, 105]),
    )
    return fig
