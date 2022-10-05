import requests
import pandas as pd


STARTING_DRIVERS = 20
RACE_INFORMATION_KEYS = tuple(["season", "round", "raceName"])
RESULTS_KEY = "Results"


def get_api_data(api_url: str, parameters: dict) -> dict:
    """
    Extracts api data formatting it as a json.
    """
    response = requests.get(api_url, parameters)
    if not response.ok:
        return dict()
    else:
        return response.json()


def unnest_ergast_api_race_data(raw_api_data: dict) -> dict:
    """
    Unnests the race data from the ergast API response.
    """
    return raw_api_data["MRData"]["RaceTable"]["Races"][0]


def get_race_information_df(
    labels: tuple, unnested_race_data: dict, starting_drivers: int
) -> pd.DataFrame:
    """
    Docstring
    """
    data = {
            l: [unnested_race_data[l]
            for i in range(starting_drivers)] for l in labels
    }
    return pd.DataFrame(data)


def get_race_results(
    api_url: str = "https://ergast.com/api/f1/current/last/results.json",
    api_parameters: dict = None,
    race_information_keys: tuple = RACE_INFORMATION_KEYS,
    results_key: str = RESULTS_KEY,
    starting_drivers: int = STARTING_DRIVERS,
) -> pd.DataFrame:
    """
    The function only works with race results from the ergast API.
    Should take url as argument in case data for a specific race is required.
    The function only works with json data.
    """
    if not api_url.endswith(".json"):
        print(f"The url needs to end with '.json'.")
        return pd.DataFrame()

    raw_data = get_api_data(api_url, api_parameters)
    unnested_data = unnest_ergast_api_race_data(raw_data)

    df_race_information = get_race_information_df(
        race_information_keys, unnested_data, starting_drivers
    )

    df_results = pd.json_normalize(unnested_data[results_key])

    return df_race_information.merge(
        df_results, how="inner", right_index=True, left_index=True
    )


if __name__ == "__main__":
    df = get_race_results()
    print(df.head())
