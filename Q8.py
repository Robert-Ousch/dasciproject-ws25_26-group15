import requests
import pandas as pd
import matplotlib.pyplot as plt
from requests.auth import HTTPBasicAuth
import os

header = {'x-apisports-key': os.getenv("API_FOOTBALL_KEY") }


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


    df = pd.DataFrame.from_dict(result)
    return df
