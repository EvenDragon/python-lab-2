import csv
from datetime import datetime
from pathlib import Path

import pytest

from streamstats.errors import InvalidEventError
from streamstats.models import SkippedEvent
from streamstats.parsers import parse_csv, parse_files


def test_parse_csv_valid(tmp_path: Path) -> None:
    path = tmp_path / "events.csv"

    with open(path, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "level", "source", "message"])
        writer.writerow([
            "2026-10-23T12:00:00+03:00",
            "ERROR",
            "app",
            "GTA6",
        ])
    events = list(parse_csv(str(path), SkippedEvent()))

    assert len(events) == 1
    assert events[0].timestamp == datetime.fromisoformat("2026-10-23T12:00:00+03:00")
    assert events[0].level == "ERROR"
    assert events[0].source == "app"
    assert events[0].message == "GTA6"

def test_parse_csv_empty_file(tmp_path: Path) -> None:
    path = tmp_path / "empty.csv"
    path.write_text("", encoding="utf-8")

    events = list(parse_csv(str(path), SkippedEvent()))

    assert events == []


def test_parse_csv_broken_line(tmp_path: Path) -> None:
    path = tmp_path / "broken.csv"
    path.write_text(
        "timestamp,level,source,message\n"
        "2026-10-23T12:00:00+03:00,ERROR,app\n",
        encoding="utf-8",
    )

    with pytest.raises(InvalidEventError) as error:
        list(parse_csv(str(path), SkippedEvent()))

    assert f"{path}:2:" in str(error.value)


def test_parse_csv_multiple_files(tmp_path: Path) -> None:
    first_path = tmp_path / "first.csv"
    second_path = tmp_path / "second.csv"
    header = "timestamp,level,source,message\n"

    first_path.write_text(
        header + "2026-10-23T12:00:00+03:00,ERROR,db,Error\n",
        encoding="utf-8",
    )
    second_path.write_text(
        header + "2026-10-23T12:01:00+03:00,INFO,app,Start\n",
        encoding="utf-8",
    )

    events = list(parse_files([str(first_path), str(second_path)], "csv", SkippedEvent()))

    assert len(events) == 2
    assert events[0].source == "db"
    assert events[1].source == "app"

def test_parse_csv_unicode(tmp_path: Path) -> None:
    path = tmp_path / "unicode.csv"
    source = "приложение"
    message = "Браво 🎵"

    with open(path, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "level", "source", "message"])
        writer.writerow([
            "2026-10-23T12:00:00+03:00",
            "INFO",
            source,
            message,
        ])

    events = list(parse_csv(str(path), SkippedEvent()))

    assert len(events) == 1
    assert events[0].source == source
    assert events[0].message == message


def test_parse_csv_skip_invalid(tmp_path: Path) -> None:
    path = tmp_path / "events.csv"
    path.write_text(
        "timestamp,level,source,message\n"
        "2026-10-23T12:00:00+03:00,INFO,app,Start\n"
        "2026-10-23T12:01:00+03:00,INVALID,app,Broken\n"
        "2026-10-23T12:02:00+03:00,ERROR,db,Error\n",
        encoding="utf-8",
    )
    skipped = SkippedEvent()

    events = list(parse_csv(str(path), skipped, skip_invalid=True))

    assert len(events) == 2
    assert events[0].source == "app"
    assert events[1].source == "db"
    assert skipped.skipped == 1
