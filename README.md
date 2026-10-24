# About this project

This is my second Python project. It is a CLI program that reads events from CSV and JSONL files and creates a JSON report with statistics. Files are processed one record at a time without loading the whole file into memory.

## Prerequisites

* Python 3.12 or newer
* uv
* typer
* pydantic
* loguru
* pytest for tests

Install the project and its dependencies from the project directory:

```bash
uv sync
```

## How to use it

Program can recognize the following commands:

```bash
uv run python -m streamstats analyze INPUT [INPUT ...] --format csv|jsonl --output REPORT.json
uv run python -m streamstats --help
uv run python -m streamstats analyze --help
```

`INPUT` is a path to an input file. All files in one command must have the format selected with `--format`.

The default output path is `report.json`.

### Examples

Analyze one JSONL file:

```bash
uv run python -m streamstats analyze events.jsonl --format jsonl --output report.json
```

Analyze several CSV files:

```bash
uv run python -m streamstats analyze first.csv second.csv --format csv --output report.json
```

Skip invalid records and continue processing:

```bash
uv run python -m streamstats analyze events.jsonl --format jsonl --skip-invalid
```

### Input files

Each event must contain four fields:

| Field | Description |
| --- | --- |
| timestamp | Date and time in ISO 8601 format |
| level | DEBUG, INFO, WARNING, ERROR or CRITICAL |
| source | A non-empty string |
| message | A string |

CSV files must have a header:

```csv
timestamp,level,source,message
2026-10-23T12:00:00+03:00,INFO,app,Start
2026-10-23T12:01:00+03:00,ERROR,db,Connection failed
```

JSONL files contain one JSON object per line:

```jsonl
{"timestamp":"2026-10-23T12:00:00+03:00","level":"INFO","source":"app","message":"Start"}
{"timestamp":"2026-10-23T12:01:00+03:00","level":"ERROR","source":"db","message":"Connection failed"}
```

Input files use UTF-8 encoding. Use timestamps with the same timezone convention: do not mix timestamps with and without timezone information.

### Report

The JSON report contains:

* Total number of valid events.
* Number of events by level and by source.
* First and last timestamps.
* Top 5 sources of ERROR events.
* Top 5 sources of CRITICAL events.
* Number of skipped records.

Statistics from all input files are combined into one report. Empty input produces zero events, empty counters and `null` timestamps.

### Invalid records

By default, processing stops at the first invalid record. The program prints the file path and line number and exits with code `2`.

With `--skip-invalid`, invalid records are skipped with a WARNING in the log. Their number is included in the report as `skipped_lines`.

## Project files

| File | Description |
| --- | --- |
| src/streamstats/__main__.py | CLI commands and error handling |
| src/streamstats/models.py | Event validation and skipped-record counter |
| src/streamstats/parsers.py | CSV, JSONL and multiple-file reading |
| src/streamstats/analysis.py | Statistics calculation |
| src/streamstats/report.py | Saving the JSON report |
| src/streamstats/errors.py | Application exceptions |
| src/streamstats/constants.py | Shared constants and logging level type |
| tests/ | Parser and CLI tests |

## Tests

Run all tests:

```bash
uv run python -m pytest -v
```


### Few words about processing

Parsers use generators to pass events to the analyzer one at a time. Pydantic validates event fields, and Counter collects statistics during a single pass. JSONL records are decoded with json.loads, while CSV records are read with csv.DictReader, which handles quoted fields and commas inside messages.
