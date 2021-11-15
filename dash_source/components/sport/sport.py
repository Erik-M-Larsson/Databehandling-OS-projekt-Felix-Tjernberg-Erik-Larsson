import pandas as pd
import plotly_express as px
from dash import dcc, html
from dash.dependencies import Input, Output

from app import app
from components.sport.load_sport_data import load_sport_data_frames
from components.sport.sport_list import sport_list
import components.sport.plots as plots


sport_data_dictionaries = load_sport_data_frames()


anatomy_filename = "assets/anatomy.svg"

medals_filename = "assets/os-medals.svg"

layout = html.Div(
    [
        dcc.Store(id="sport-data-frame"),
        dcc.Store(id="sport-medal-frame"),
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
        html.H2("Medal race"),
        html.Img(
            id="medals-svg",
            src=medals_filename,
            alt="Illustration of silver, gold and bronze olympic medals",
        ),
        dcc.Graph(id="sport-medal-race"),
        html.H2("Player type"),
        html.Section(
            [
                html.Img(
                    id="anatomy-svg",
                    src=anatomy_filename,
                    alt="Illustration of female and male anatomy",
                ),
                dcc.Graph(id="sport-gender-pie"),
                dcc.Graph(id="sport-age-histogram"),
                html.Div(
                    [
                        dcc.Graph(id="sport-height-histogram"),
                        dcc.Graph(id="sport-weight-histogram"),
                    ],
                    id="height-and-width-histograms",
                ),
            ],
            id="player-type",
        ),
    ],
    id="sport",
)


@app.callback(Output("sport-data-frame", "data"), Input("sport-dropdown", "value"))
def load_data_frame(value):
    if value == None:
        return

    return sport_data_dictionaries[f"{format(value.title())}"]["general"].to_json()


@app.callback(Output("sport-medal-frame", "data"), Input("sport-dropdown", "value"))
def load_medal_frame(value):
    if value == None:
        return

    return sport_data_dictionaries[f"{format(value.title())}"]["medal_count"].to_json()


@app.callback(Output("sport-name", "children"), Input("sport-dropdown", "value"))
def update_heading_text(value):
    if value == None:
        return "Sport stats"

    return value


@app.callback(
    Output("sport-age-histogram", "figure"),
    Input("sport-data-frame", "data"),
)
def update_age_histogram(data):
    if data == None:
        return px.histogram()

    sport_data_frame = pd.read_json(data)
    return plots.age_histogram(sport_data_frame)


@app.callback(
    Output("sport-gender-pie", "figure"),
    Input("sport-data-frame", "data"),
)
def update_gender_pie(data):
    if data == None:
        return px.pie()

    sport_data_frame = pd.read_json(data)
    return plots.gender_pie(sport_data_frame)


@app.callback(
    Output("sport-height-histogram", "figure"),
    Input("sport-data-frame", "data"),
)
def update_height_histogram(data):
    if data == None:
        return px.histogram()

    sport_data_frame = pd.read_json(data)
    return plots.height_histogram(sport_data_frame)


@app.callback(
    Output("sport-weight-histogram", "figure"),
    Input("sport-data-frame", "data"),
)
def update_weight_histogram(data):
    if data == None:
        return px.histogram()

    sport_data_frame = pd.read_json(data)
    return plots.weight_histogram(sport_data_frame)


@app.callback(
    Output("sport-medal-race", "figure"),
    Input("sport-medal-frame", "data"),
)
def update_medal_race(data):
    if data == None:
        return px.bar()

    sport_data_frame = pd.read_json(data)
    return plots.medal_race_plot(sport_data_frame)
