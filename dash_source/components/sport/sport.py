import dash
import pandas as pd
import plotly_express as px
from dash import dcc, html
from dash.dependencies import Input, Output
import time

from app import app
from components.sport.load_sport_data import load_sport_data_frames
from components.sport.sport_list import sport_list
import components.sport.plots as plots


anatomy_filename = "https://raw.githubusercontent.com/Erik-M-Larsson/Databehandling-OS-projekt-Felix-Tjernberg-Erik-Larsson/de0f7d0a8dd874c37ca3ed00c72027bc72e9ef6c/dash_source/assets/anatomy.svg"

medals_filename = "https://raw.githubusercontent.com/Erik-M-Larsson/Databehandling-OS-projekt-Felix-Tjernberg-Erik-Larsson/de0f7d0a8dd874c37ca3ed00c72027bc72e9ef6c/dash_source/assets/os-medals.svg"

layout = html.Div(
    [
        dcc.Store(id="sport-data-frame"),
        dcc.Store(id="sport-medal-frame"),
        # html.P(id="sport-name"),
        html.Header(
            [
                html.H1(id="sport-name-heading"),
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


sport_data_dictionaries = load_sport_data_frames()


def get_sport_name(string):
    try:
        return string.split("/")[2].replace("-", " ").title()
    except:
        return None


def match_sport_list(string):
    return any([string == sport_name for sport_name in sport_list])


@app.callback(
    Output("url", "pathname"),
    Input("sport-dropdown", "value"),
    prevent_initial_call=True,
)
def navigate_to_sport(value):
    if any([value == sport for sport in sport_list]):
        return f"/sport-stats/{value.lower().replace(' ', '-')}"

    return dash.no_update


@app.callback(
    Output("sport-data-frame", "data"), Input("sport-name", "sport-name-test")
)
def load_data_frame(value):
    if value == None:
        return

    return sport_data_dictionaries[f"{format(value.title())}"]["general"].to_json()


@app.callback(Output("sport-medal-frame", "data"), Input("sport-name", "children"))
def load_medal_frame(value):
    if value == None:
        return

    return sport_data_dictionaries[f"{format(value.title())}"]["medal_count"].to_json()


@app.callback(
    Output("sport-name-heading", "children"),
    Input("url", "pathname"),
    Input("height-and-width-histograms", "children"),
    # prevent_initial_call=True,
)
def update_heading_text(value, children):
    time.sleep(1)  # Hack to make callback load last
    if not match_sport_list(get_sport_name(value)):
        return "Sport stats"

    return get_sport_name(value)


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
