import pandas as pd
from utilities.create_medal_count_data_frame import create_medal_count_data_frame


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
