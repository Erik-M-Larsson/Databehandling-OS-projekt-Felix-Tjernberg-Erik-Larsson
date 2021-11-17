import pandas as pd
from components.sport.load_sport_data import create_medal_count_data_frame


def load_landing_data_frames():
    os_data_raw = pd.read_csv("./data/athlete_events.csv")

    # print("load_landing ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    landing_dict = {
        "world_medal_race": create_medal_count_data_frame(os_data_raw),
        "sweden_medal_count": swedish_medal_counts(os_data_raw)
        # for sport_key, sport_data_frame in sport_dict_general.items()
    }

    return landing_dict


def swedish_medal_counts(data):
    swedish_athletes = data.query("NOC == 'SWE'")
    swedish_medals = swedish_athletes.drop_duplicates(
        subset=["Year", "Event", "Medal"], inplace=False
    )

    return swedish_medals.dropna(subset=["Medal"]).sort_values("Medal", ascending=False)
