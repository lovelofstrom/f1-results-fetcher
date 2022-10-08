### F1 Results Fetcher
Small program that extracts F1 results from the Ergast API.

## Instructions
Execute ./setup.sh after the repo is downloaded to install dependencies in a
virtual environment.

Execute / Schedule execution ./run.sh to fetch the weekly F1 Results.

The results are saved in a .csv file in ./data/ by default.

Flexibility when running ./run.sh or ./f1_results_fetcher/__main__.py:
 * Specify the full directory to the file you want to save the results to with the `--dst` argument: `--dst /Documents/F1Results/latest_f1_results.csv`. <b>Note: Only .csv is currently supported.</b>
 * Specify whether to replace/create a new results file or append to an existing results file with the `--write` argument: `--write append`
 * Decide which race to fetch results from with the `--url` argument. The url is structure is https://ergast.com/api/f1/YYYY/ROUND/results.json passing the following argument to ./run.sh or ./f1_results_fetcher/__main__.py will fetch the results from round 5 in the 2008 season: `--url https://ergast.com/api/f1/2008/5/results.json` <b>Note: The url is suffixed by .json, which is the supported format in this program. Drop the .json suffix to view the results on the website.</b>

## Notes
Only tested on macOS.
