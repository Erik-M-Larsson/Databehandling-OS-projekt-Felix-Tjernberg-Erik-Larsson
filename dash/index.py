import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_html_components as html

from app import app
from components import landing
from components.sport import sport


app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)


@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(path_name):
    path_name_split = path_name.split("/")

    # Renders sport component if adress includes sport else landing component
    if path_name_split[1] == "sport":
        return sport.layout
    else:
        return landing.layout


if __name__ == "__main__":
    app.run_server(debug=True)
