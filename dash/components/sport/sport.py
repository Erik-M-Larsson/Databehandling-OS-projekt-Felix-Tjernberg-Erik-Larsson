import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from components.sport.load_sport_data import load_sport_data


layout = html.Div(
    [
        html.H1(id="sport-name"),
        html.P(id="sport-data-frame"),
        dcc.Link("Back", href="/"),
    ]
)


@app.callback(Output("sport-name", "children"), Input("url", "pathname"))
def parse_path_name(pathname):
    split_path_name = pathname.split("/")
    return split_path_name[2]


@app.callback(Output("sport-data-frame", "children"), Input("url", "pathname"))
def load_data_frame(pathname):
    split_path_name = pathname.split("/")
    data_frame = load_sport_data(split_path_name[2])
    return data_frame
