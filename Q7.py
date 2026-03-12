import requests
import pandas as pd
import matplotlib.pyplot as plt


def df7():
    result = {}
    # year: goal_away per team

    alternatives = ['1. FSV Mainz 05', 'TSG 1899 Hoffenheim', 'TSG Hoffenheim', 'Bayer 04 Leverkusen', \
                'FC Bayern München', 'Borussia Dortmund', 'Borussia Mönchengladbach', \
                'VfL Wolfsburg']

    for x in range(15):
        season = 2010 + x
        result[season] = {}
        url = "https://api.openligadb.de/getmatchdata/bl1/" + str(season)
        response = requests.get(url)
        response = response.json()

        # get total number of goals away
        for match in response:
            teamName2 = match['team2']['teamName']
            if teamName2 == 'TSG 1899 Hoffenheim':
                teamName2 = 'TSG Hoffenheim'
            if teamName2 in alternatives:
                if teamName2 not in result[season].keys():
                    result[season][teamName2] = 0
            
                goals = match ['goals']
                score1 = 0
                score2 = 0        
                for goal in goals:
                    score1new = goal ['scoreTeam1'] 
                    score2new = goal ['scoreTeam2']
                    if score1new != None and score2new != None:
                        if score1new > score1:      # home goal team 1
                            score1 = score1new
                        else:       # away goal team 2
                            result[season][teamName2] += 1
                            score2 = score2new

    df = pd.DataFrame.from_dict(result)
    df = df.transpose()
    return df
