from dash import html
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly_express as px

from app import app
from components.sport.load_sport_data import create_medal_count_data_frame
from components.sport.plots import medal_race_plot

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
                                {"label": f"Year {number}", "value": "placeholder"}
                                for number in range(4)
                            ],
                            value="Year 0",
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
