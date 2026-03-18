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
6. Which teams scored goals at home turf most often?
7. During the last 15 seasons, when did FC Bayern München score goals most often in their opponent’s city?
8. How does the venue capacity influence the win rate of the away team?

For this project, the main data source is the API api.openligadb.de, which contains historic data of matches, teams and goals. The API v3.football.api-sports.io is used for the venue capacity. Finally, geocoding-api.open-meteo.com incluces weather data, more specifically rainfall and precipitation for given coordinates.
The lollipop plot is implemented based on https://hi-artemii.medium.com/vertical-lollipop-chart-in-plotly-python-minimal-code-example-1e1bca0b1261.

### Data pipeline
We split our research questions up between the team members, so the data pipeline is not uniform for all questions. Following methods were used to utilize the data sources for each question:
1. Q1: Collection: Multiple API calls, getting the match data of the 1. Bundesliga for each year (10/11 - 24/25).
       Selection: Only the teams and goals of each match are selected  
       Integration/Transformation: Data is read from a json file and then put into dictionaires containing each teams scores for different time intervals (binning) as well as their total number of matches played and goals scored  
       Cleaning: Data which is incomplete (i.e the minute the goals was scored is missing) is ignored, as it happens very rarely  
       Visualization: Using plotly express, make bar charts comparing the calculated values for each timeslot and each team  
RQ2
- Collection: We collected all matches from the 2004-2025 Bundesliga seasons as well as the involved teams from the openligadb api, then found the coordinates where  each match happened using the open-meteo geocoding api, then found the weather during each match using the open-meteo weather api.
- Selection: We were only interested in the time, place and number of goals for each match. We also only looked at precipitation during each match, instead of all weather conditions. 
- Cleaning: Single matches with missing location, time or result had to be discarded, though the location could often be inferred from the name of the first mentioned team, which is always the home team. Teams with less than 30 matches are also discarded entirely.
- Integration/Transformation: The nested response structure from the openligadb api is flattened into a dictionary with 2d arrays, the result is saved as json for use in the website, so as to not cause an unnecessary flood of requests whenever it is started.
- Visualization: The data is displayed as a box plot, showing the typical distribution of goals scored for each team during games with more or less than any given amount of precipitation.
RQ3
- Collection: Same as RQ2
- Selection: Same as RQ2
- Cleaning: Same as RQ2, except we didn't discard teams with less than 30 matches
- Integration/Transformation: The nested response structure from the openligadb api is flattened into a dictionary with 1d arrays, then saved as json. The matches are aggregated into buckets based on precipitation with a bucket size of 0.1mm.
- Visualization: The average number of goals for matches in each respective bucket is displayed as a scatter plot, with a regression line highlighting a slight upward trend.
4.  Collection: 
    Selection: 
    Cleaning: 
    Integration/Transformation:
    Visualization: 
5.  Collection: 
    Selection: 
    Cleaning: 
    Integration/Transformation:
    Visualization: 
RQ6
- Collection: We accessed the data source openligadb API and the match data for the seasons 2010 to 2024
- Selection: Gathered teams playing in each season and their goals scored at home 
- Cleaning: There was no data cleaning needed
- Integration/Transformation: Our function reads the data from a json file and then returns the selected data in a DataFrame
- Visualization: This function is imported on the website, using the function plot_category_lollipop to display the graph

RQ7
- Collection: We accessed the data source openligadb API and the match data for the seasons 2010 to 2024
- Selection: Gathered teams paying in each season and their goals scored away, only selected the seven teams playing in the 1. Bundesliga in every of those seasons
- Cleaning: We ignored all other teams, as they are not helpful in answering this question
- Integration/Transformation: Our function reads the data from a json file and then returns the selected data in a DataFrame
- Visualization: This function is imported on the website, using plotly express to display the data in a line graph

RQ8
- Collection: By hand, we mapped the team id of football API to those of openligadb API. This mapper as used to construct a dictionary of venues with their capacity (from football API) and the name of the home team (from openligadb API). Then accessed the data source openligadb API and the match data for the last 15 seasons.
- Selection: Store won and total matches per away team, where we had a venue capacity for the match
- Cleaning: Ignored all matches, where we had no venue capacity given
- Integration/Transformation: The extracted data is used to compute the win rate per team and venue capacity, which is then stored in a text file
- Visualization: This file is imported on the website, using plotly express to display the data in a heatmap 

### Website build
The website is built and deployed using gunicorn and render, installing a recent python version and dependencies from our requirements.txt.  
Using app.py as a frame around our actual content pages, we add every page using dash.register_page() to our page container and iteratively link to it with dcc.Link


### Website usage
Our homepage consists of a navigational menu, allowing you to choose between the pages of each research question or the section about our team. The homepage also displays the milestones and issues during the project timeline and the description of the data sources.
Each research question is displayed on its own page with the title and explanatory text sections about the graph and the calculations. There is at least one dynamic visualization per question with dynamic elements such as dropdown menus, sliders or radio buttons. 
In general, there are eight different graph types, for example bar charts and a stacked bar chart, boxplots, scatterplots. We also use a slope graph, a lollipop graph, a line graph and a heatmap to best visualize the data.

### LLM
All lines of code, that are either directly from LLM or developed with the help of a LLM are marked accordingly.

### About us
This project is created as part of the Data Science Project of the winter semester 2025/26 from Cristian-Albrechts-University in Kiel. Our group is number 15 and the team members are Hauke Busch, Jakob Erichsen, Alexander Liebler and Robert Ousch.
