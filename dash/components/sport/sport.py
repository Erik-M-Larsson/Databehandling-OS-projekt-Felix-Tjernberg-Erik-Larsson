import dash_core_components as dcc
import dash_html_components as html
import plotly_express as px
import pandas as pd
from dash.dependencies import Input, Output

from app import app
from components.sport.load_sport_data import load_sport_data_frames
from components.sport.sport_list import sport_list

sport_data_frames = load_sport_data_frames()

layout = html.Div(
    [
        dcc.Store(id="sport-data-frame"),
        html.H1(id="sport-name"),
        dcc.Dropdown(
            clearable=False,
            id="sport-dropdown",
            value="Aeronautics",
            options=[{"label": f"{sport}", "value": sport} for sport in sport_list],
        ),
        dcc.Graph(id="sport-histogram"),
        dcc.Link("Back", href="/"),
    ]
)


@app.callback(Output("sport-data-frame", "data"), Input("sport-dropdown", "value"))
def load_data_frame(value):
    sport_data_frame = sport_data_frames[f"{value.capitalize()}"]
    return sport_data_frame.to_json()


@app.callback(Output("sport-name", "children"), Input("sport-dropdown", "value"))
def update_heading_text(value):
    return value


@app.callback(
    Output("sport-histogram", "figure"),
    Input("sport-data-frame", "data"),
)
def update_histogram_graph(data):
    sport_data_frame = pd.read_json(data)
    figure = px.histogram(
        sport_data_frame,
        x="Age",
        labels={"count": "Antal"},
        title="Age distribution",
    )
    return figure
