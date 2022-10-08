import pandas as pd
import requests


def validate_api_url(api_url: str) -> bool:
    """
    The program only supports f1 results fetched from the Ergast API in a
    .json format. The function validates that the url has the expected start
    and end of a valid url.
    """
    return (
        api_url.startswith("http://ergast.com/api/f1/")
        or api_url.startswith("https://ergast.com/api/f1/")
    ) and api_url.endswith("results.json")


def get_api_data(api_url: str) -> dict:
    """
    Extracts api data formatting it as a json.
    """
    response = requests.get(api_url)
    if not response.ok:
        return dict()
    else:
        return response.json()


def unnest_ergast_api_race_data(raw_api_data: dict) -> dict:
    """
    Unnests the race data from the ergast API response.
    """
    assert len(raw_api_data["MRData"]["RaceTable"]["Races"]) == 1
    return raw_api_data["MRData"]["RaceTable"]["Races"][0]


def build_race_information(
    unnested_race_data: dict,
    starting_drivers_n: int,
) -> pd.DataFrame:
    """
    Gets race information that are constant throughout the race. Examples:
    name of the race, season, round. The data returned is determined by
    labels argument and is multiplied by the number of starting drivers.
    """
    data = {
        l: [
            unnested_race_data[l]
            # one row per starting driver for easy merge w/ race results
            for i in range(starting_drivers_n)
        ]
        for l in ["season", "round", "raceName"]
    }
    return pd.DataFrame(data)


def build_race_results(unnested_race_data: dict) -> pd.DataFrame:
    """
    Builds a pd.DataFrame with the season, round, race name, and race results
    by driver.
    """
    # extracts the results by driver from the unnested race data
    df_results = pd.json_normalize(unnested_race_data["Results"])
    drivers_n = len(df_results.index)
    df_race_information = build_race_information(
        unnested_race_data,
        drivers_n,
    )

    df_race_results = df_race_information.merge(
        df_results, how="inner", right_index=True, left_index=True
    )

    assert drivers_n == len(df_race_results.index)

    return df_race_results


def get_race_results(api_url: str) -> pd.DataFrame:
    """
    The function only works with race results from the Ergast API.
    Should take url as argument in case data for a specific race is required.
    The function only works with json data.
    """
    assert validate_api_url(api_url), f"{api_url} is invalid."

    raw_data = get_api_data(api_url)
    unnested_data = unnest_ergast_api_race_data(raw_data)

    df_race_results = build_race_results(unnested_data)

    return df_race_results


if __name__ == "__main__":
    df = get_race_results(
        "https://ergast.com/api/f1/current/last/results.json",
    )
    print(df.head())
