def swedish_medal_counts(data):
    swedish_athletes = data.query("NOC == 'SWE'")
    swedish_medals = swedish_athletes.drop_duplicates(
        subset=["Year", "Event", "Medal"], inplace=False
    )

    return swedish_medals.dropna(subset=["Medal"]).sort_values("Medal", ascending=False)
