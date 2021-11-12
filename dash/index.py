from dash import dcc
from dash import html
from dash.dependencies import Input, Output

from app import app
from components import landing
from components.sport import sport


app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)
app.title = "Olympic sports dash app"


@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(path_name):
    if path_name == "/sport-stats":
        return sport.layout
    else:
        return landing.layout


if __name__ == "__main__":
    app.run_server(debug=True)
