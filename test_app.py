from dash import Dash, html

app = Dash(__name__)

app.layout = html.Div("Hello World")

if __name__ == "__main__":
    app.run(
        debug=False,
        use_reloader=False,   # disable extra process
        port=8060,
        host="127.0.0.1"
    )