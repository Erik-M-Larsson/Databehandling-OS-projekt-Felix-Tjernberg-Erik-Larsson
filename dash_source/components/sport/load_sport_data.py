import os
import pandas as pd
import itertools


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
            "Year",
            "Season",
            "Sport",
            "City",
            "Sex",
        ],
        inplace=True,
    )
    data_cleaned.sort_values(by="Games", inplace=True)
    data_cleaned.drop_duplicates(
        subset=["NOC", "Games", "Event", "Medal"], inplace=True
    )

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

    return medal_count


def swedish_medal_counts(swedish_athletes):
    swedish_medals = swedish_athletes.drop_duplicates(
        subset=["Year", "Event", "Medal"], inplace=False
    )
    swedish_medal_counts = (
        swedish_medals.groupby(by=["Year", "Medal"], sort=False).count().reset_index()
    )
    swedish_medal_counts.sort_values(
        by=["Medal", "Year"], axis=0, ascending=[False, True], inplace=True
    )
    return swedish_medal_counts
