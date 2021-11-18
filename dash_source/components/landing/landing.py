import plotly_express as px
from dash import dcc, html
from dash.dependencies import Input, Output

from app import app
from components.landing.year_list import year_list
from components.landing.load_landing_data import (
    swedish_medal_counts,
    load_landing_data_frames,
)
import utilities.plots as plots


layout = html.Div(
    [
        # dcc.Store(id="world-medal-frame"),
        html.H1("Sweden is best per capita*"),
        html.Aside([html.P("* Best per capita in top 10 of medal taking countries")]),
        html.Section(
            [
                html.Div(
                    [
                        html.H2("World medal race top 10"),
                        dcc.Loading(
                            [
                                dcc.Graph(id="world-medal-race"),
                            ],
                            type="circle",
                            color="white",
                        ),
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
                            value=1912,  # Best year for Sweden and in Stockholm
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


landing_data_dictionaries = load_landing_data_frames()


@app.callback(
    Output("world-medal-race", "figure"),
    Input(
        "sweden-medals-at-year", "children"
    ),  # Hack to make callback fire when component is loaded
)
def update_world_medal_race(children):
    return plots.medal_race_plot(landing_data_dictionaries["world_medal_count"])


@app.callback(
    Output("sweden-medals-at-year", "figure"),
    Input("year-dropdown", "value"),
)
def update_sweden_medals_at_year(year):
    if year == None:
        return px.bar()

    return plots.swedish_medals_barplot(
        swedish_medal_counts(landing_data_dictionaries["sweden_medal_count"]), year
    )
