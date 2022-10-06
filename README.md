### F1 Results Fetcher
Small program that extracts F1 results from the ergast API.

## Instructions
Execute setup.sh after the repo is downloaded to install dependencies in a
virtual environment.

Execute / Schedule execution run.sh to fetch the weekly F1 Results.

The results are saved in a .csv file in ./data/ by default.

Flexibility when running run.sh / __main__.py
Decide results file destionation with --dst arg.
Decide whether to append or create a new file with the --save arg.
Decide which race to fetch results from with the --url arg.

## Notes
Only tested on MacOs.

## TODOs
[] validate file formats
[] validate columns in generic file name creation
[] enforce .csv format
[] enforce .json urls
[] and maybe some more.