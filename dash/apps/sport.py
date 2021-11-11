import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

layout = html.Div(
    [
        html.H1(id="sport-name"),
        dcc.Link("Back", href="/"),
    ]
)


@app.callback(Output("sport-name", "children"), Input("url", "pathname"))
def parse_path_name(pathname):
    split_path_name = pathname.split("/")
    return split_path_name[2]
