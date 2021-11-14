from dash import html
from dash import dcc, html
from dash.dependencies import Input, Output

from app import app


layout = html.Div(
    [
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
                            id="sport-dropdown",
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
