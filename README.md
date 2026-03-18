# Read Me

## Rain, timing or home advantage? What Influences goals and victories in the bundesliga.

### Introduction
This project is about the 1. Bundesliga of football in Germany. This project discusses different influences on the number of goals or the victories of the teams, e.g. scored goals, the timeline of the match, the rainfall, the venue or the location at home vs. away.

Following research questions are answered:
1. During the last 15 seasons, inspecting 15 minute intervalls, when are the most goals scored during a match? How does this differ between teams?
2. How does high rainfall during a match influence the win rate of certain German teams? 
3. How does high rainfall during a match influence the total number of goals scored? 
4. Over the span of the last 15 seasons, Which teams most frequently achieve comeback victories in the second half?
5. Is there a statistically significant relationship between the timing of the first conceded goal and the probability of a match ending in defeat? 
6. Which teams scored goals at home turf most often in 2024?
7. During the last 15 seasons, when did FC Bayern München score goals most often in their opponent’s city (vs. home)?
8. How does the venue capacity influence the win rate of the away team during the years 2022-2024?

For this project, the main data source is the API api.openligadb.de, which contains historic data of matches, teams and goals. The API v3.football.api-sports.io is used for the venue capacity. Finally, geocoding-api.open-meteo.com incluces weather data, more specifically rainfall and precipitation for given coordinates.
The lollipop plot is implemented based on https://hi-artemii.medium.com/vertical-lollipop-chart-in-plotly-python-minimal-code-example-1e1bca0b1261.

### Data pipeline
The following steps were taken to arrive at our solutions:
1. Q1: Collection: Multiple API calls, getting the match data of the 1. Bundesliga for each year (10/11 - 24/25).
       Selection: Only the teams and goals of each match are selected  
       Integration/Transformation: Data is read from a json file and then put into dictionaires containing each teams scores for different time intervals (binning) as well as their total number of matches played and goals scored  
       Cleaning: Data which is incomplete (i.e the minute the goals was scored is missing) is ignored, as it happens very rarely  
       Visualization: Using plotly express, make bar charts comparing the calculated values for each timeslot and each team    

### Website build
The website is built and deployed using gunicorn and render, installing a recent python version and dependencies from our requirements.txt.  
Using app.py as a frame around our actual content pages, we add every page using dash.register_page() to our page container and iteratively link to it with dcc.Link


### Website usage
todo Showcase how to use your web application and the highlights

### LLM
All lines of code, that are either directly from LLM or developed with the help of a LLM are marked accordingly.

### About us
This project is created as part of the Data Science Project of the winter semester 2025/26 from Cristian-Albrechts-University in Kiel. Our group is number 15 and the team members are Hauke Busch, Jakob Erichsen, Alexander Liebler and Robert Ousch.
