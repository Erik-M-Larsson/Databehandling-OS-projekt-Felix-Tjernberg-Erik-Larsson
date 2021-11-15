import os
import pandas as pd
import itertools


def load_sport_data_frames():
    os_data_raw = pd.read_csv("./data/athlete_events.csv")

    medal_count_all = create_medal_count_data_frame(os_data_raw)

    create_sport_data_frame = lambda sport_name, df: df.query(
        f'Sport == "{sport_name}"'
    )

    sport_dict = {
        sport: {
            "general": create_sport_data_frame(sport, os_data_raw),
            "medal_count": create_sport_data_frame(sport, medal_count_all),
        }
        for sport in list(os_data_raw["Sport"].unique())
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
