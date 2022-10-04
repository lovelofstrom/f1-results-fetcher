from pathlib import Path
from f1_results_fetcher import get_race_results


# default project directory for results to be stored.
RESULTS_PATH = Path(".").absolute() / "data"


if __name__ == "__main__":
    df = get_race_results()
    if df.empty:
        print("No results data.")
    else:
        try:
            # creates a file name based on the first values of the first
            # two columns of the dataframe.
            part_a, part_b = df.iloc[0, 0:2]
            file_path = RESULTS_PATH / f"{part_a}{part_b}.csv"
        except (IndexError, ValueError):
            print("The expected data was not found.")
        if file_path.exists():
            print("Data has already been fetched.")
        else:
            df.to_csv(file_path, index=False)
            print(f"F1 results were saved in {file_path}")
