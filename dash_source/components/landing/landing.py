import importlib
import os
from dash import html
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly_express as px
import json

from app import app
from components.sport.load_sport_data import create_medal_count_data_frame
from components.sport.plots import medal_race_plot
from components.landing.year_list import year_list
from components.landing.load_swed_data import swedish_medal_counts
from components.landing.swed_plots import swedish_medals_barplot

os_data_raw = pd.read_csv("./data/athlete_events.csv")

layout = html.Div(
    [
        dcc.Store(id="world-medal-frame"),
        html.H1("Sweden is best per capita*"),
        html.Aside([html.P("* Best per capita in top 10 of countries")]),
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
                            "Sweden's youngest medal",
                        ),
                        html.P(
                            "Nils skoglund at the age of 13 took silver in diving year 1920",
                        ),
                    ],
                    className="glass-background",
                ),
                html.Div(
                    [
                        html.H3(
                            "Sweden's oldest medal",
                        ),
                        html.P(
                            "Oscar Gomer Swahn at the age of 72 took silver in shooting year 1920",
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
    return create_medal_count_data_frame(os_data_raw).to_json()


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

    return swedish_medals_barplot(swedish_medal_counts(os_data_raw), year)
