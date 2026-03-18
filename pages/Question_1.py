import requests, json
import pandas as pd
import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px

### All code written here by Robert Ousch

### Calculations ###
def df1():
    # 1. Gather scores of teams and total scores in intervals
    # for last 15 seasons (season 10/11 to 24/25)

    # Bundesliga stats Bookkeeping
    total_matches = 0
    total_goals = {15:0, 30:0, 45:0, 60:0, 75:0, 90:0, 105:0}
    teams = {}

    # Compute number of goals scored in each interval over the last 15 years
    # for every team as well as the Bundesliga as a whole
    for i in range(0,15):
        year = 2010 + i
        url = 'https://api.openligadb.de/getmatchdata/bl1/' + str(year) 
        response = json.loads(requests.get(url).text)
        
        for match in response:
            # ID and current score Bookkeeping
            t1_id = match['team1']['teamId'] 
            t2_id = match['team2']['teamId']
            t1_score = 0
            t2_score = 0

            # Add new entries to teams dict
            if t1_id not in teams.keys():
                teams[t1_id] = {'name':match['team1']['teamName'],
                                'matches':0,
                                'total':{15:0, 30:0, 45:0, 60:0, 75:0, 90:0, 105:0}}

            if t2_id not in teams.keys(): 
                teams[t2_id] = {'name':match['team2']['teamName'],
                                'matches':0,
                                'total':{15:0, 30:0, 45:0, 60:0, 75:0, 90:0, 105:0}}

            #No. of matches Bookkeeping
            teams[t1_id]['matches'] += 1 
            teams[t2_id]['matches'] += 1 
            total_matches += 1
            
            # Sum goals for intervals
            for goal in match['goals']:
                # Ignore data that is incomplete
                if type(goal['matchMinute']) == int:
                    interval = ((goal['matchMinute'] // 15) + 1) * 15
                    # Increment goal at interval for team that scored
                    if goal['scoreTeam1'] > t1_score:  
                        t1_score = goal['scoreTeam1'] 
                        teams[t1_id]['total'][interval] += 1
                    else:
                        t2_score = goal['scoreTeam2']
                        teams[t2_id]['total'][interval] += 1
                    # Increment total goals scored in the Bundesliga    
                    total_goals[interval] += 1

    
    # 2. Calculate statistics for every team over all years.
    # prc = percentage. Looks at percentage of goals scored
    # in an interval compared to total goals scored,
    # i.e. "When team x scores a goal, how likely is it
    # that it happened in the first/second/last 15 minutes?"
    # gpi = goals per interval. Looks at the amount of goals scored
    # in an interval over all matches
    # i.e. "How many goals does a team score
    # in the first/second/last 15 minutes in any given match?"

    # Bookeeping for the whole Bundesliga statistics
    total_gpi = {15:0, 30:0, 45:0, 60:0, 75:0, 90:0, 105:0}
    total_prc = {15:0, 30:0, 45:0, 60:0, 75:0, 90:0, 105:0}
    number_of_goals = sum(total_goals.values())

    for interval in total_goals.keys(): 
        total_gpi[interval] = round(total_goals[interval] / (total_matches * 2), 4)
        total_prc[interval] = round((total_goals[interval] / number_of_goals) * 100, 4)

    # Calculate statistics for every team
    for team in teams:
        teams[team]['gpi'] = {15:0, 30:0, 45:0, 60:0, 75:0, 90:0, 105:0}
        teams[team]['prc'] = {15:0, 30:0, 45:0, 60:0, 75:0, 90:0, 105:0}
        tg = sum(teams[team]['total'].values())

        for interval in teams[team]['total'].keys():
            # These don't work when split into two lines
            teams[team]['gpi'][interval] = round(teams[team]['total'][interval] / teams[team]['matches'], 4)  
            teams[team]['prc'][interval] = round((teams[team]['total'][interval] / tg) * 100, 4)
    
    # Create Bundesliga "team" with id 0 based on calculated stats.
    teams[0] = {'name':'Bundesliga', 'matches':total_matches,
                'total':total_goals, 'gpi':total_gpi, 'prc': total_prc}
    
    # Create dataframe
    team_names = []
    minutes = []
    gpi_values = []
    prc_values = []
    for id in teams:
        team_names += [teams[id]['name']] * 7 # Once for every interval
        minutes += [str(x) for x in teams[id]['gpi'].keys()]
        gpi_values += teams[id]['gpi'].values()
        prc_values += teams[id]['prc'].values()


    d = {'Team': team_names,
        'Minute': minutes, 
        'Goals': gpi_values,
        'Percentage':prc_values}

    df = pd.DataFrame(d)
    return df

df1 = df1()
fig1 = px.bar(df1, x = 'Minute', y = 'Percentage', color = 'Team',
    barmode = 'group', range_x = [15,105], text = 'Percentage')

### Page Layout ###
dash.register_page(__name__)

layout = html.Div([
    html.H3('Question 1: Inspecting 15 minute intervalls,\
        when during the last 15 years (seasons 10/11 to 24/25)\
        were the most goals scored?', id = 'Q1Question'),
    html.P(['"Goals" shows the number of goals scored in an average game,',
        html.Br(),
        '"Percentage" shows the percentage of goals\
        scored in that time interval'],
        id = 'Q1RadioTip'),
    html.Div(dcc.Dropdown(df1['Team'][::7],
                          value = ['Bundesliga'],
                          multi = True,
                          id = 'Q1TeamDropdown')),
    html.Div(dcc.RadioItems(options = ['Goals', 'Percentage'],
                            value = 'Goals',
                            id = 'Q1Radio')),
    html.Div(dcc.Graph(id = 'Q1Barchart',
                       figure = fig1)),
    html.P(['Calculated by summing all goals scored by a team\
        in a specific timeslot during the last 15 seasons,',
        html.Br(),
        'then dividing by amount of matches played for "Goals"\
        and total goals scored for "Percentage"'],
        id = 'Q1Details')],
    id = 'Q1Div', style = {'background': '#f9f9f9', 'border': '1px solid #e0e0e0', 'borderRadius': '6px',
        'padding': '14px 18px', 'marginBottom': '12px', 'marginTop': '20px'})

### Callback ###
@callback(
    Output('Q1Barchart', 'figure'),
    Input('Q1Radio', 'value'),
    Input('Q1TeamDropdown', 'value')
)
def update_Q1(ratio, selected_teams):
    df_temp = pd.DataFrame({'Minute':[], 'Goals':[], 'Team':[], 'Percentage':[]})
    for team in selected_teams:
        rows = df1.loc[df1['Team'] == team]
        df_temp = pd.concat([df_temp, rows], ignore_index = True)
    fig1 = px.bar(df_temp, x = 'Minute', y = ratio,
                  color = 'Team', barmode = 'group', text = ratio)
    return fig1