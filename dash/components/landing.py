from dash import html
from dash.dependencies import Input, Output

from app import app


layout = html.Div(
    [
        html.H1("Sverige är bra fan"),
        html.A("Go to sport stats", href="/sport-stats"),
    ],
    id="landing",
)
