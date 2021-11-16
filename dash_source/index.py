from dash import dcc, html
from dash.dependencies import Input, Output

from app import app

from components.sport import sport
from components.landing import landing

os_rings_filename = "assets/os-rings.svg"

app.layout = html.Div(
    [
        html.Nav(
            [
                html.Img(src=os_rings_filename, alt="Image of olympic rings"),
                html.Ul(
                    [
                        html.Li([html.A("Home", href="/")]),
                        html.Li([html.A("Sport stats", href="/sport-stats")]),
                    ]
                ),
            ]
        ),
        html.Main(
            [
                dcc.Location(id="url", refresh=False),
                html.Article(id="page-content"),
            ]
        ),
    ],
)
app.title = "Olympic sports dash app"


@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(path_name):
    if path_name == "/sport-stats":
        return sport.layout
    else:
        return landing.layout


if __name__ == "__main__":
    app.run_server(debug=True)
