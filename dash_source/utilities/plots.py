import plotly_express as px


def age_histogram(df):
    fig = px.histogram(
        df,
        x="Age",
        labels={"Sex": "Gender"},
        color="Sex",
        barmode="group",
        title="Age distribution",
        color_discrete_map={"M": "#636efa", "F": "#ef553b"},
    )
    fig.update_layout(
        {"paper_bgcolor": "rgba(0,0,0,0)"},
        title={"x": 0.5},
        legend={"y": 0.5},
        yaxis_title="",
    )
    return fig


def gender_pie(df):
    gender_count = (
        df[df["Sex"] == "M"]["Sex"].count(),
        df[df["Sex"] == "F"]["Sex"].count(),
    )

    fig = px.pie(
        df,
        values=gender_count,
        names=["Male", "Female"],
        title="Gender distribution",
        color_discrete_map={"Male": "#636efa", "Female": "#ef553b"},
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
        labels={"Sex": "Gender"},
        title="Height distribution",
        color="Sex",
        barmode="group",
        color_discrete_map={"M": "#636efa", "F": "#ef553b"},
    )
    fig.update_layout(
        {"paper_bgcolor": "rgba(0,0,0,0)"},
        title={"x": 0.5},
        legend={"y": 0.5},
        yaxis_title="",
    )
    return fig


def medal_race_plot(df):
    """Animated barplot of accumulated number of medals per NOC"""

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
        labels={"Cumulative_medals": "Medals", "NOC": "Country code"},
    )

    # Sort y-axis
    fig.update_layout(title={"x": 0.5}, yaxis={"categoryorder": "total ascending"})

    # Change animation duration
    numb_of_games = len(df["Year"].unique())

    if numb_of_games > 1:
        duration = 1920 - 30 * numb_of_games
        fig.layout.updatemenus[0].buttons[0].args[1]["frame"][
            "duration"
        ] = duration  # Ref: https://community.plotly.com/t/how-to-slow-down-animation-in-plotly-express/31309

    # Show only top ten
    numb_of_noc = len(df["NOC"].unique())
    fig.update_yaxes(range=(max(numb_of_noc - 10.5, -0.5), numb_of_noc - 0.5))

    # Set x-ticks
    fig.update_xaxes(range=(0, max(df["Cumulative_medals"]) + 0.5), tick0=0)

    return fig


def swedish_medals_barplot(data, year):
    fig = px.histogram(
        data.query("Year == @year"),
        x="Medal",
        color="Medal",
        color_discrete_map={
            "Gold": "gold",
            "Silver": "silver",
            "Bronze": "darkgoldenrod",
        },
        barmode="relative",
        labels={"Sex": "Gender"},
    )
    fig.update_layout(
        title={"text": f"Medals {year}", "x": 0.5},
        xaxis_title="",
        yaxis_title="",
        bargap=0.2,
        showlegend=False,
    )

    return fig


def weight_histogram(df):
    fig = px.histogram(
        df,
        x="Weight",
        title="Weight distribution",
        color="Sex",
        barmode="group",
        labels={"Sex": "Gender"},
        color_discrete_map={"M": "#636efa", "F": "#ef553b"},
    )
    fig.update_layout(
        {"paper_bgcolor": "rgba(0,0,0,0)"},
        title={"x": 0.5},
        legend={
            "y": 0.5,
        },
        yaxis_title="",
    )
    return fig
