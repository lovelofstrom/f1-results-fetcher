import requests
import json
import pandas as pd


def get_api_data(api_url: str, parameters: dict) -> dict:
    """
    Extracts api data to a json object.
    """
    response = requests.get(api_url, parameters)
    if not response.ok:
        return {}
    else:
        return response.json()


def get_formatted_results(raw_results_data: dict) -> pd.DataFrame:
    """"
    Docstring
    Figure out if it should be a pd.DataFrame
    / if I should construct a csv in a different way.
    should probably add keys as an arg for unpacking to avoid magic numbers.
    """
    # remove magic numbers at some point
    results_data = {
        "season": [],
        "round": [],
        "race_name": [],
        "position": [],
        "points": [],
        "driver": [],
        "team": []
    }

    # season and round_ are strings in the data. convert?
    season = raw_results_data["MRData"]["RaceTable"]["Races"][0]["season"]
    round_ = raw_results_data["MRData"]["RaceTable"]["Races"][0]["round"]
    race_name = raw_results_data["MRData"]["RaceTable"]["Races"][0]["raceName"]

    # try/except or just check if keys exist / otherwise return empty df?
    for i in raw_results_data["MRData"]["RaceTable"]["Races"][0]["Results"]:
        results_data["season"].append(season)
        results_data["round"].append(round_)
        results_data["race_name"].append(race_name)
        results_data["position"].append(i["position"])
        results_data["points"].append(i["points"])
        results_data["driver"].append(i["Driver"]["code"])
        results_data["team"].append(i["Constructor"]["name"])

    df = pd.DataFrame(results_data)

    return df


# should results url be a "constant"?
def get_race_results(
        api_url: str = "https://ergast.com/api/f1/current/last/results.json",
        api_parameters: dict = None
):
    """
    The function only works with race results from the ergast API.
    Should take url as argument in case data for a specific race is required.
    """
    # maybe write test for url to check if it has the expected format.
    raw_data = get_api_data(api_url, api_parameters)
    results = get_formatted_results(raw_data)
    return results

if __name__ == "__main__":
    # file name should be named YYYYMMDD / and or race name.
    df = get_race_results()
    print(df.head())
