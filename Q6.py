import requests
import pandas as pd
import matplotlib.pyplot as plt

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