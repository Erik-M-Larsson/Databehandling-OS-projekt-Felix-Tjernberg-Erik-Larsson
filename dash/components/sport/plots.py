import plotly_express as px
import pandas as pd
import itertools


def age_histogram(df):
    fig = px.histogram(
        df, x="Age", labels={"Age": "Ålder", "count": "Antal"}, title="Åldersfördelning"
    )
    fig.update_layout(title={"x": 0.5})
    return fig


def gender_pie(df):
    gender_count = (
        df[df["Sex"] == "M"]["Sex"].count(),
        df[df["Sex"] == "F"]["Sex"].count(),
    )
    fig = px.pie(
        df, values=gender_count, names=["Män", "Kvinnor"], title="Könsfördelning"
    )
    fig.update_layout(title={"x": 0.5}, legend={"y": 0.5})
    return fig


def height_histogram(df):
    fig = px.histogram(
        df,
        x="Height",
        labels={"Height": "Längd", "count": "Antal", "Sex": "Kön", "M": "Män"},
        title="Längdfördelning",
        color="Sex",
        barmode="group",
    )
    fig.update_layout(title={"x": 0.5})
    return fig


def weight_histogram(df):
    fig = px.histogram(
        df,
        x="Weight",
        labels={"Weight": "Vikt", "count": "Antal", "Sex": "Kön", "M": "Män"},
        title="Viktfördelning",
        color="Sex",
        barmode="group",
    )
    fig.update_layout(title={"x": 0.5})
    return fig


def medal_race_plot(sport_data: "DataFrame") -> None:
    """Skapa ett rörligt stapeldiagram över akumulerat antal medaljer per land"""

    # Clean data
    data_cleaned = sport_data.dropna(subset=["Medal"])
    data_cleaned.drop(
        columns=[
            "ID",
            "Name",
            "Age",
            "Height",
            "Weight",
            "Team",
            "Year",
            "Season",
            "City",
            "Sex",
            "Sport",
        ],
        inplace=True,
    )
    data_cleaned.sort_values(by="Games", inplace=True)
    data_cleaned.drop_duplicates(subset=["Games", "Event", "Medal"], inplace=True)

    # Calculate accumulated medals per NOC
    medal_count = data_cleaned.groupby(by=["Games", "NOC"]).count().reset_index()
    games_noc_combinations = pd.DataFrame(
        itertools.product(data_cleaned["NOC"].unique(), data_cleaned["Games"].unique()),
        columns=["NOC", "Games"],
    )
    medal_count = (
        medal_count.merge(games_noc_combinations, on=["Games", "NOC"], how="right")
        .sort_values(["Games", "NOC"])
        .fillna(0)
    )
    medal_count["Cumulative_medals"] = medal_count.groupby("NOC")["Medal"].cumsum()

    # Plot bar diagram animation
    fig = px.bar(
        medal_count,
        x="Cumulative_medals",
        y="NOC",
        color="NOC",
        animation_group="NOC",
        animation_frame="Games",
        # title="Medal race",
    )

    # Sort y-axis
    fig.update_layout(title={"x": 0.5}, yaxis={"categoryorder": "total ascending"})

    # Change animation duration
    numb_of_games = len(medal_count["Games"].unique())
    duration = 1920 - 30 * numb_of_games
    print("numb_of_games: ", numb_of_games, "\n", "duration: ", duration)
    fig.layout.updatemenus[0].buttons[0].args[1]["frame"][
        "duration"
    ] = duration  # Ref: https://community.plotly.com/t/how-to-slow-down-animation-in-plotly-express/31309

    # Show only top ten
    numb_of_noc = len(medal_count["NOC"].unique())
    fig.update_yaxes(range=(max(numb_of_noc - 10.5, -0.5), numb_of_noc - 0.5))

    # Set x-ticks to integers
    fig.update_xaxes(
        range=(0, max(medal_count["Cumulative_medals"]) + 0.5), dtick=1, tick0=0
    )

    return fig
