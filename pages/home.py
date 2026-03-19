import dash
from dash import html

dash.register_page(__name__, path='/')

card = {'background': '#f9f9f9', 'border': '1px solid #e0e0e0', 'borderRadius': '6px',
        'padding': '14px 18px', 'marginBottom': '12px'}
label = {'fontWeight': '600', 'marginBottom': '6px', 'fontSize': '15px'}


def ele_card(title, text):
    return html.Div([
        html.Div(title, style=label),
        html.P(text, style={'margin': '0', 'color': '#444'})
    ], style=card)


layout = html.Div([
    ele_card('Week 1: Topic brainstorming',
        'The three different topics we came up with were: '
        'Public transport, crime rates, football in Germany. '
        'The main issue was finding optimal APIs to answer all of our questions. '),
    ele_card('Week 2: Answering the research questions',
        'One of our data sources, football API, does not provide as much historic data '
        'as we originally planned with. '
        'The provided range was not enough to answer following questions: '
        '4. How many goals are scored on average before a player is transferred to '
        'another team? '
        '5. What is the correlation between the win rate of a coach`s team and '
        'the coach`s time at the team? '
        'Those research questions were replaced with new ones. '
        'We were able to use the data sources to answer three of our research questions. '),
    ele_card('Week 3: Basic website',
        'We used the data sources to answer the remaining five research questions, '
        'including the two new questions. '
        'We built a basic website and added some static visualizations. '
        'Following issues occurred: '
        'Some of our implementations had to be changed to using the Pandas DataFrame, '
        'so that we could use plotly for the graphs on the website. '
        'Another challenge were the graphs using multiple interactive elements. '
        'The Gunicorn start command was not correct and had to be changed and '
        'the wait times per deploy were quite long and made testing difficult. '),
    ele_card('Week 4: Final website and poster',
        'Our website now contains at least one dynamic visualization and an explanatory '
        'section per research question and more than four different graph types. '
        'We chose six of our research questions for our scientific poster. '),
    ele_card('Description of data sources',
        'For this project, the main data source is the API api.openligadb.de, '
        'which contains historic data of matches, teams and goals. '
        'The API v3.football.api-sports.io is used for the venue capacity. '
        'Finally, geocoding-api.open-meteo.com incluces weather data, more specifically '
        'rainfall and precipitation for given coordinates. '
        'The lollipop plot is implemented based on https://hi-artemii.medium.com/vertical-'
        'lollipop-chart-in-plotly-python-minimal-code-example-1e1bca0b1261.'),
])
