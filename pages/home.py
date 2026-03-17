import dash
from dash import html

dash.register_page(__name__, path='/')

layout = html.Div([
    html.H1('This is our Home page', style = {'textAlign':'center'}),
    html.Div('Description of data sources'),
    html.P('For this project, the main data source is the API api.openligadb.de,' \
        'which contains historic data of matches, teams and goals.' \
        'The API v3.football.api-sports.io is used for the venue capacity. '\
        'Finally, geocoding-api.open-meteo.com incluces weather data, more specifically'\
        'rainfall and precipitation for given coordinates.'\
        'The lollipop plot is implemented based on https://hi-artemii.medium.com/vertical-'\
        'lollipop-chart-in-plotly-python-minimal-code-example-1e1bca0b1261.')
])