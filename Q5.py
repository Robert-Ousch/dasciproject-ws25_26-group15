import requests
import pandas as pd

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
