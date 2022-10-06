import requests
import pandas as pd


STARTING_DRIVERS_N = 20
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


def get_race_information(
    labels: tuple, unnested_race_data: dict, starting_drivers: int
) -> pd.DataFrame:
    """
    Gets race information that are constant throughout the race. Examples:
    name of the race, season, round. The data returned is determined by
    labels argument and is multiplied by the number of starting drivers.
    """
    data = {l: [unnested_race_data[l]
            for i in range(starting_drivers)] for l in labels}
    return pd.DataFrame(data)


def get_race_results(
    api_url: str,
    api_parameters: dict = None,
) -> pd.DataFrame:
    """
    The function only works with race results from the ergast API.
    Should take url as argument in case data for a specific race is required.
    The function only works with json data.
    """
    # mayne ends with results.json?
    if not api_url.endswith(".json"):
        print(f"The url needs to end with '.json'.")
        return pd.DataFrame()

    raw_data = get_api_data(api_url, api_parameters)
    unnested_data = unnest_ergast_api_race_data(raw_data)

    df_race_information = get_race_information(
        RACE_INFORMATION_KEYS, unnested_data, STARTING_DRIVERS_N
    )

    df_results = pd.json_normalize(unnested_data[RESULTS_KEY])

    df = df_race_information.merge(
        df_results, how="inner", right_index=True, left_index=True
    )

    df.loc[:, "id"] = df.index.map(
        lambda x: df.iloc[x][RACE_INFORMATION_KEYS[0]]
        + df.iloc[x][RACE_INFORMATION_KEYS[1]]
        +
        # adds one to the index so that the row starts at 1, not 0.
        str(x + 1)
    )

    df = df.set_index("id")

    return df


if __name__ == "__main__":
    df = get_race_results(
        "https://ergast.com/api/f1/current/last/results.json")
    print(df.head())
