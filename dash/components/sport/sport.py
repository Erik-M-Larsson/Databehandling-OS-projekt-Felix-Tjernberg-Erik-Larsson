import pandas as pd
import plotly_express as px
from dash import html
from dash import dcc
from dash.dependencies import Input, Output

from app import app
from components.sport.load_sport_data import load_sport_data_frames
from components.sport.sport_list import sport_list


sport_data_frames = load_sport_data_frames()


layout = html.Div(
    [
        dcc.Store(id="sport-data-frame"),
        html.Header(
            [
                html.H1(id="sport-name"),
                dcc.Dropdown(
                    clearable=False,
                    id="sport-dropdown",
                    options=[
                        {"label": f"{sport}", "value": sport} for sport in sport_list
                    ],
                    placeholder="Select a sport",
                ),
            ]
        ),
        dcc.Graph(id="sport-histogram"),
        dcc.Link("Back", href="/"),
    ]
)


@app.callback(Output("sport-data-frame", "data"), Input("sport-dropdown", "value"))
def load_data_frame(value):
    if value == None:
        return

    sport_data_frame = sport_data_frames[f"{value.capitalize()}"]
    return sport_data_frame.to_json()


@app.callback(Output("sport-name", "children"), Input("sport-dropdown", "value"))
def update_heading_text(value):
    if value == None:
        return "Sport stats"

    return value


@app.callback(
    Output("sport-histogram", "figure"),
    Input("sport-data-frame", "data"),
)
def update_histogram_graph(data):
    if data == None:
        return px.histogram()

    sport_data_frame = pd.read_json(data)
    figure = px.histogram(
        sport_data_frame,
        x="Age",
        labels={"count": "Antal"},
        title="Age distribution",
    )
    return figure
