import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_html_components as html

from app import app
from apps import landing, sport


app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)


@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if pathname == "/":
        return landing.layout
    elif pathname == "/sport":
        return sport.layout
    else:
        return landing.layout


if __name__ == "__main__":
    app.run_server(debug=True)
