import plotly_express as px


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
    )
    fig.update_layout(
        title={"text": f"Medals {year}", "x": 0.5},
        xaxis_title="",
        yaxis_title="",
        bargap=0.2,
        showlegend=False,
    )

    return fig
