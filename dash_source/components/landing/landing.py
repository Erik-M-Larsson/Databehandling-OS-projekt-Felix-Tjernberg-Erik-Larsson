from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly_express as px
import json

from app import app

from components.sport.plots import medal_race_plot
from components.landing.year_list import year_list
from components.landing.load_landing_data import (
    swedish_medal_counts,
    load_landing_data_frames,
)
from components.landing.swed_plots import swedish_medals_barplot

landing_data_dictionaries = load_landing_data_frames()

layout = html.Div(
    [
        dcc.Store(id="world-medal-frame"),
        html.H1("Sweden is best per capita*"),
        html.Aside([html.P("* Best per capita in top 10 of medal taking countries")]),
        html.Section(
            [
                html.Div(
                    [
                        html.H2("World medal race top 10"),
                        dcc.Graph(id="world-medal-race"),
                    ]
                ),
                html.Div(
                    [
                        html.H2("Sweden medals per year"),
                        dcc.Dropdown(
                            clearable=False,
                            id="year-dropdown",
                            options=[
                                {"label": year, "value": year} for year in year_list
                            ],
                            value=1912,  # Best game for Sweden and in Stockholm
                        ),
                        dcc.Graph(id="sweden-medals-at-year"),
                    ]
                ),
            ],
            id="landing-graphs",
        ),
        html.H2("Sweden fun facts"),
        html.Section(
            [
                html.Div(
                    [
                        html.H3(
                            "Sweden's youngest medal taker",
                        ),
                        html.P(
                            "Sweden's youngest medal taker took silver in diving year 1920 at the age of 13",
                        ),
                    ],
                    className="glass-background",
                ),
                html.Div(
                    [
                        html.H3(
                            "Sweden's oldest medal taker",
                        ),
                        html.P(
                            "Sweden's oldest medal taker took silver in shooting year 1920 at the age of 72",
                        ),
                    ],
                    className="glass-background",
                ),
            ],
            id="fun-facts",
        ),
    ],
    id="landing",
)


@app.callback(Output("world-medal-frame", "data"), Input("fun-facts", "value"))
def load_medal_frame(value):
    return landing_data_dictionaries["world_medal_race"].to_json()


@app.callback(
    Output("world-medal-race", "figure"),
    Input("world-medal-frame", "data"),
)
def update_world_medal_race(data):
    if data == None:
        return px.bar()

    sport_data_frame = pd.read_json(data)
    return medal_race_plot(sport_data_frame)


@app.callback(
    Output("sweden-medals-at-year", "figure"),
    Input("year-dropdown", "value"),
)
def update_sweden_medals_at_year(year):
    if year == None:
        return px.bar()

    return swedish_medals_barplot(
        swedish_medal_counts(landing_data_dictionaries["sweden_medal_count"]), year
    )
