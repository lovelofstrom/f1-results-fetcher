import argparse
from pathlib import Path

import pandas as pd

from f1_results_fetcher import get_race_results

LATEST_F1_RESULTS_URL = "https://ergast.com/api/f1/current/last/results.json"
DEFAULT_RESULTS_PATH = Path(__file__).absolute().parent.parent / "data"


def get_default_file_name(
    race_results: pd.DataFrame,
    file_ext: str = ".csv",
) -> Path:
    """
    Creates a file path based on the names of the first value in the
    first two columns of the pd.DataFrame.
    """
    assert len(race_results.columns) >= 2
    season, round_ = df.iloc[0, 0:2]
    return DEFAULT_RESULTS_PATH / f"{season}{round_}{file_ext}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--url",
        help="Results url",
        default=LATEST_F1_RESULTS_URL,
    )
    parser.add_argument(
        "--dst",
        help="full file dir to the output file including .csv ext",
        default=None,
    )
    parser.add_argument(
        "--write",
        type=str.lower,
        default="replace",
        choices=["replace", "append"],
        help=("Creates a new results file or appends to an existing results "
              "file."),
    )
    args = parser.parse_args()

    df = get_race_results(args.url)
    if args.dst is None:
        file_dst_path = get_default_file_name(df)
    else:
        file_dst_path = Path(args.dst)

    assert str(file_dst_path).endswith(".csv"), "unspported file format."
    if args.write == "append":
        include_header = not file_dst_path.exists()
        df.to_csv(file_dst_path, mode="a", header=include_header)
    else:
        df.to_csv(file_dst_path)
