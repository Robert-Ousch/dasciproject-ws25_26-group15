import requests, json
import pandas as pd
import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px


### Calculations ###
def df8():

    ### Map the team IDs of footbal.api to those of api.openliga

    teamIDmapper = {
        '157': 40,      # München
        '158': None,    # Düsseldorf, not in 1bl
        '159': 54,      # Hertha
        '160': 112,     # Freiburg
        '161': 131,     # Wolfsburg
        '162': 134,     # Bremen
        '163': 87,      # Mönchengladbach
        '164': 81,      # Mainz
        '165': 7,       # Dortmund
        '167': 175,     # Hoffenheim
        '168': 6,       # Leverkusen
        '169': 91,      # Frankfurt
        '170': 95,      # Augsburg
        '172': 16,      # Stuttgart
        '173': 1635,    # Leipzig
        '174': 9,       # Schalke
        '175': None,    # Hamburg, not in 1bl
        '176': 129,     # Bochum
        '180': 199,     # Heidenheim
        '181': 118,     # Darmstadt
        '182': 80,      # Union Berlin
        '186': 98,      # St. Pauli
        '191': 104,     # Holstein Kiel
        '192': 65,      # Köln
        '1660': None    # not in 1bl
    }



    ### get all venues of 2022-2024

    venues = {}     # venueID according to openligadb: capacity, name
    for x in range(3):
        season = 2022 + x
        url = "https://v3.football.api-sports.io/teams?league=78&season=" + str(season)
        response = requests.get(url, headers=header)
        response = response.json()

        for team_venue in response ['response']:
            teamID = str(team_venue['team']['id'])
            venueID = teamIDmapper [teamID]
            if venueID not in venues.keys() and venueID != None: 
                capacity = team_venue['venue']['capacity']
                name = team_venue['team']['name']
                venues[venueID] = {'capacity': capacity, 'name': name}


    ### get number of wins and matches per venue for all teams 

    wins = {}       # teamName: capacity: wins
    total = {}      # teamName: capacity: total
    result = {}     # teamName: capacity: winrate

    for x in range(15):
        season = 2009 + x
        url = "https://api.openligadb.de/getmatchdata/bl1/" + str(season)
        response = requests.get(url)
        response = response.json()

        for match in response:
            # get ID away team & venueID, if new add to result 
            teamID2 = match['team2']['teamId']
            venueID = match['team1']['teamId']
            if venueID in venues.keys() and teamID2 in venues.keys():       
                teamName2 = match['team2']['teamName']
                capacity = venues[venueID]['capacity']
                if teamName2 not in result.keys():        # new team
                    wins[teamName2] = {}
                    total[teamName2] = {}
                    result[teamName2] = {}
                if capacity not in result[teamName2].keys():         # new venue for this team
                    wins[teamName2][capacity] = 0
                    total[teamName2][capacity] = 0
                    result[teamName2][capacity] = 0

                # get number of wins and total matches
                matchResult = match['matchResults'][0]
                if matchResult['pointsTeam2'] >= 3:     # win away team
                    wins[teamName2][capacity] += 1
                total[teamName2][capacity] += 1

    # compute win rate
    for team in result.keys():
        for venue in result[team].keys():
            nr_wins = wins[team][venue]
            nr_total = total[team][venue]
            result[team][venue] = nr_wins / nr_total


    with open('data_Q8.txt', 'w') as file:
        file.write(json.dumps(result))
    
    df = pd.DataFrame.from_dict(result)
    return df

with open("data_Q8.txt", "r") as file:
    data_Q8 = json.loads(file.read())
df8 = pd.DataFrame(data_Q8)
df8 = df8.sort_index()
#df8.index = df8.index.astype(int)

### Page Layout ###
dash.register_page(__name__)

layout = html.Div([
            html.H3('Question 8: How does the venue capacity influence the win rate of the \
                away team for the seasons 2022-2024?'),
            html.P('We wanted to analyze, whether the venue capacity influences the \
	            win rate of the away team.\
                Our source provides capacity information for the seasons 2022 – 2024. \
                The dynamic heatmap displayes the win rate of the away team \
                for the selected venue capacities and teams.\
                The win rate is calculated as the matches won at the venue by the given\
                team divided by all matches played at the venue by the given team.\
                The heatmap is missing values for the combination of venue and team, \
                where the team is the home team at the specific venue or\
                where the team did not play any match at the specific venue. '),
            #html.P("Select upper and lower bounds for the venue capacity:"),
            #dcc.Checklist(
                #options = ['15000', '17810', '22467', '27599', '29564', '30000', '30164', '30210', '30662', \
                #'34034', '34700', '42358', '47069', '50076', '54057', '58000', '60469', '62278', '74667', \
                #'75024', '81365'],
                #value = ['15000', '17810', '22467', '27599', '29564', '30000', '30164', '30210', '30662', \
                #'34034', '34700', '42358', '47069', '50076', '54057', '58000', '60469', '62278', '74667', \
                #'75024', '81365'],
                #inline = True,
                #id = 'component8_1'),
            html.P("Select one or more teams to compare:"),
            dcc.Dropdown(
                options = ['1. FC Heidenheim 1846', '1. FC Köln',	'1. FC Union Berlin', '1. FSV Mainz 05', \
                    'Bayer 04 Leverkusen', 'Borussia Dortmund', 'Borussia Mönchengladbach', \
                    'Eintracht Frankfurt', 'FC Augsburg', 'FC Bayern München', 'FC Schalke 04', 'FC St. Pauli', \
                    'Hertha BSC', 'RB Leipzig', 'SC Freiburg', 'SV Darmstadt 98', 'SV Werder Bremen', \
                    'TSG Hoffenheim', 'VfB Stuttgart', 'VfL Bochum', 'VfL Wolfsburg'], 
                value = ['FC Bayern München'],
                multi = True,
                id = 'component8_2'),
            html.Div(dcc.Graph(id = 'graph8', figure = px.imshow(df8))) 
        ], id = 'Q8Div')

### Callback ###
@callback(
    Output(component_id = 'graph8', component_property = 'figure'),
    #Input(component_id = 'component8_1', component_property = 'value'),
    Input(component_id = 'component8_2', component_property = 'value')
)
def upgrade_graph_8(team_chosen):
    fig8 = px.imshow(df8[team_chosen], color_continuous_scale = 'Plotly3', \
        aspect = 'auto')      
    fig8.update_yaxes(nticks = 21)
    fig8.update_xaxes(nticks = len(team_chosen))
    fig8.update_layout(
        xaxis_title = 'Teams', 
        yaxis_title = 'Venue capacity'
    )
    return fig8 
''' 
def upgrade_graph_8(capacity_chosen, team_chosen):
    df_temp = pd.DataFrame({})
    #rows = df8.loc[(df8.index >= slider[0]) & (df8.index <= slider[1])]
    rows = df8.loc[(capacity_chosen in df8.index)]
    df_temp = pd.concat([df_temp, rows]) 
    fig8 = px.imshow(df8[team_chosen])
    fig8.update_xaxes(nticks = len(team_chosen))
    return fig8 
'''