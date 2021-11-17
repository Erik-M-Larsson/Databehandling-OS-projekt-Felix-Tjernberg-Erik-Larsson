import itertools
import pandas as pd


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

    sport_dicts = {
        sport_key: {
            "general": sport_data_frame,
            "medal_count": create_medal_count_data_frame(sport_data_frame),
        }
        for sport_key, sport_data_frame in sport_dict_general.items()
    }

    return sport_dicts


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
    medal_count.drop(columns=["Event", "Medal"], inplace=True)

    # Filter out only the NOC:s that appear in top ten over all years
    noc_top_ten_all_years = pd.DataFrame()

    for year in medal_count["Year"].unique():
        noc_top_ten_year = (
            medal_count.query("Year == @year")
            .sort_values(by="Cumulative_medals", ascending=False)["NOC"]
            .head(10)
        )  # All NOC in top ten each year

        noc_top_ten_all_years = pd.concat(
            [noc_top_ten_all_years, noc_top_ten_year],
            axis=0,
        )  # All NOC in top ten over all years

    noc_top_ten_all_years.drop_duplicates(inplace=True)
    noc_top_ten_all_years.columns = ["NOC"]
    medal_count_top_ten = noc_top_ten_all_years.merge(medal_count, how="left", on="NOC")

    return medal_count_top_ten
