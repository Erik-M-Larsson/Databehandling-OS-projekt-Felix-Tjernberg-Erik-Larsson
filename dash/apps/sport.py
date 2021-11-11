import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app

layout = html.Div([html.H1("I'm sport"), dcc.Link("Back", href="/")])


# @app.callback(
# Output("app-1-display-value", "children"), Input("app-1-dropdown", "value")
# )
# def display_value(value):
# pass
