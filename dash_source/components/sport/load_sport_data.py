import os
import pandas as pd
import itertools

from pandas.core.frame import DataFrame


def load_sport_data_frames():
    os_data_raw = pd.read_csv("./data/athlete_events.csv")

    create_sport_specific_data_frame = lambda sport_name, df: df.query(
        f'Sport == "{sport_name}"'
    )

    sport_list = list(os_data_raw["Sport"].unique())

    sport_dict_general = {
        sport_name: create_sport_specific_data_frame(sport_name, os_data_raw)
        for sport_name in sport_list
    }

    sport_dict = {
        sport_key: {
            "general": sport_data_frame,
            "medal_count": create_medal_count_data_frame(sport_data_frame),
        }
        for sport_key, sport_data_frame in sport_dict_general.items()
    }

    return sport_dict


def create_medal_count_data_frame(df):

    # Clean data
    data_cleaned = df.dropna(subset=["Medal"])
    data_cleaned.drop(
        columns=[
            "ID",
            "Name",
            "Age",
            "Height",
            "Weight",
            "Team",
            "Season",
            "Sport",
            "City",
            "Sex",
            "Games",
        ],
        inplace=True,
    )
    data_cleaned.sort_values(by="Year", inplace=True)
    data_cleaned.drop_duplicates(subset=["NOC", "Year", "Event", "Medal"], inplace=True)

    # Calculate accumulated medals per NOC
    medal_count = data_cleaned.groupby(by=["Year", "NOC"]).count().reset_index()
    games_noc_combinations = pd.DataFrame(
        itertools.product(data_cleaned["NOC"].unique(), data_cleaned["Year"].unique()),
        columns=["NOC", "Year"],
    )
    medal_count = (
        medal_count.merge(games_noc_combinations, on=["Year", "NOC"], how="right")
        .sort_values(["Year", "NOC"])
        .fillna(0)
    )
    medal_count["Cumulative_medals"] = medal_count.groupby("NOC")["Medal"].cumsum()

    top_list = pd.DataFrame()
    # print("top_list", "\n", top_list)

    for year in medal_count["Year"].unique():
        top_ten_year = (
            medal_count.query("Year == @year")
            .sort_values(by="Cumulative_medals", ascending=False)["NOC"]
            .head(10)
        )
        # print("year", year, "\n", "top_ten_year", "\n", top_ten_year, "\n")
        top_list = pd.concat(
            [top_list, top_ten_year],
            axis=0,
        )

    top_list.drop_duplicates(inplace=True)
    top_list.columns = ["NOC"]

    apa = top_list.merge(medal_count, how="left", on="NOC")
    # print("top_list", "\n", apa["NOC"].unique().size)
    # apa["NOC"].unique()

    return apa
