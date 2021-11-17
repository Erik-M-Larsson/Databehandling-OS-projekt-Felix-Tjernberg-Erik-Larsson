import plotly_express as px
import pandas as pd
import seaborn as sns


def age_histogram(df):

    fig = px.histogram(
        df, x="Age", labels={}, color="Sex", barmode="group", title="Age distribution"
    )
    fig.update_layout(
        {"paper_bgcolor": "rgba(0,0,0,0)"},
        title={"x": 0.5},
        legend={"y": 0.5},
    )
    return fig


def gender_pie(df):
    gender_count = (
        df[df["Sex"] == "M"]["Sex"].count(),
        df[df["Sex"] == "F"]["Sex"].count(),
    )

    fig = px.pie(
        df, values=gender_count, names=["Men", "Women"], title="Gender distribution"
    )

    fig.update_layout(
        {"paper_bgcolor": "rgba(0,0,0,0)"},
        title={"x": 0.5, "y": 0.1},
        legend={"y": 0.5},
    )

    return fig


def height_histogram(df):
    fig = px.histogram(
        df,
        x="Height",
        labels={},
        title="Height distribution",
        color="Sex",
        barmode="group",
    )
    fig.update_layout(
        {"paper_bgcolor": "rgba(0,0,0,0)"},
        title={"x": 0.5},
        legend={"y": 0.5},
    )
    return fig


def weight_histogram(df):
    fig = px.histogram(
        df,
        x="Weight",
        labels={},
        title="Weight distribution",
        color="Sex",
        barmode="group",
    )
    fig.update_layout(
        {"paper_bgcolor": "rgba(0,0,0,0)"}, title={"x": 0.5}, legend={"y": 0.5}
    )
    return fig


def medal_race_plot(df):
    """Animated barplot of accumulated number of medals per NOC"""
    print("df.size", df.size)
    # Plot bar diagram animation
    fig = px.bar(
        df,
        x="Cumulative_medals",
        y="NOC",
        color="NOC",
        color_discrete_sequence=px.colors.qualitative.Alphabet,
        animation_group="NOC",
        animation_frame="Year",
        title="Medal race",
        labels={"Cumulative_medals": "Medals"},
    )

    # Sort y-axis
    fig.update_layout(title={"x": 0.5}, yaxis={"categoryorder": "total ascending"})

    # Change animation duration
    numb_of_games = len(df["Year"].unique())
    duration = 1920 - 30 * numb_of_games
    print("numb_of_games: ", numb_of_games, "\n", "duration: ", duration)
    if numb_of_games > 1:
        fig.layout.updatemenus[0].buttons[0].args[1]["frame"][
            "duration"
        ] = duration  # Ref: https://community.plotly.com/t/how-to-slow-down-animation-in-plotly-express/31309

    # Show only top ten
    numb_of_noc = len(df["NOC"].unique())
    fig.update_yaxes(range=(max(numb_of_noc - 10.5, -0.5), numb_of_noc - 0.5))
    print(
        "numb_of_noc: ",
        numb_of_noc,
        "\n",
        "Y-axis range=",
        (max(numb_of_noc - 10.5, -0.5), numb_of_noc - 0.5),
    )

    # Set x-ticks to integers
    fig.update_xaxes(
        range=(0, max(df["Cumulative_medals"]) + 0.5), tick0=0
    )  # , dtick=1

    return fig
