import requests
import pandas as pd


def get_api_data(api_url: str, parameters: dict) -> dict:
    """
    Extracts api data formatting it as a json.
    """
    response = requests.get(api_url, parameters)
    if not response.ok:
        return dict()
    else:
        return response.json()


def get_formatted_results(raw_results_data: dict) -> pd.DataFrame:
    """
    Unpacks the raw data from the ergast API and adds them to a pd.DataFrame.
    """
    if not raw_results_data:
        # return empty df if no results
        return pd.DataFrame()

    results_data = {
        "season": [],
        "round": [],
        "race_name": [],
        "driver": [],
        "team": [],
        "position": [],
        "points": [],
    }

    # unpacks data that does not change by driver
    season = raw_results_data["MRData"]["RaceTable"]["Races"][0]["season"]
    round_ = raw_results_data["MRData"]["RaceTable"]["Races"][0]["round"]
    race_name = raw_results_data["MRData"]["RaceTable"]["Races"][0]["raceName"]

    # unpacks driver data
    for i in raw_results_data["MRData"]["RaceTable"]["Races"][0]["Results"]:
        results_data["season"].append(season)
        results_data["round"].append(round_)
        results_data["race_name"].append(race_name)
        # add full name?
        results_data["driver"].append(i["Driver"]["code"])
        results_data["position"].append(i["position"])
        results_data["points"].append(i["points"])
        results_data["team"].append(i["Constructor"]["name"])

    return pd.DataFrame(results_data)


def get_race_results(
    api_url: str = "https://ergast.com/api/f1/current/last/results.json",
    api_parameters: dict = None,
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
    results = get_formatted_results(raw_data)
    return results


if __name__ == "__main__":
    df = get_race_results()
