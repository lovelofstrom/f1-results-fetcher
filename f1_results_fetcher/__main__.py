import argparse
from pathlib import Path
from f1_results_fetcher import get_race_results


LATEST_F1_RESULTS_URL = "https://ergast.com/api/f1/current/last/results.json"
DEFAULT_RESULTS_PATH = Path(__file__).absolute().parent.parent / "data"


def get_default_file_name(df, file_ext: str = ".csv") -> Path:
    """
    Creates a file path based on the names of the first value in the
    first two columns of the pd.DataFrame.
    """
    part_a, part_b = df.iloc[0, 0:2]
    return DEFAULT_RESULTS_PATH / f"{part_a}{part_b}{file_ext}"


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
        "--save",
        type=str.lower,
        default="replace",
        choices=["replace", "append"],
        help="Replaces or appends to the results file.",
    )
    args = parser.parse_args()

    df = get_race_results(args.url)

    if args.dst is None:
        pass
        file_dst_path = get_default_file_name(df)
    else:
        file_dst_path = Path(args.dst)

    if args.save == "append":
        include_header = not file_dst_path.exists()
        df.to_csv(file_dst_path, mode="a", header=include_header)
    else:
        df.to_csv(file_dst_path)
