# csv_diff_analyzer
This is a python based tool to compare and find differences between two large CSV files with millions of rows.

## Dependencies
- Python 3
- SQLite3 database
**Note:** This tool has been developed on Python 3.9.x Author can not take responsibility for other python versions.

## Input
Two CSV files. CSV files can be big and might contain millions of rows.

## Output
Excel spreadsheets under `output` directory indicating three types of changes:
- Rows deleted from old CSV file
- New rows added in new CSV file
- Rows updated from old CSV file to new CSV file

## Setup
- Python can be downloaded from this [link](https://www.python.org/downloads/)
- SQLite3 database can be downloaded from this [link](https://sqlite.org/download.html)

After installation clone the repo and run `setup.py` to install all dependent python packages.
To run the tool execute `main.py` file using Python 3.
