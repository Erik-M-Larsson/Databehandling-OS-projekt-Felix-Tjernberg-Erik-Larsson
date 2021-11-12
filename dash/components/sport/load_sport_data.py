import pandas as pd


def load_sport_data_frames():
    os_data_raw = pd.read_csv("./data/athlete_events.csv")

    create_sport_data_frame = lambda sport_name: os_data_raw.query(
        f'Sport == "{sport_name}"'
    )

    sport_dict = {
        sport: create_sport_data_frame(sport)
        for sport in list(os_data_raw["Sport"].unique())
    }

    return sport_dict
