import json
from datetime import datetime
from pathlib import Path

import pytest

from streamstats.errors import InvalidTimestampError
from streamstats.models import SkippedEvent
from streamstats.parsers import parse_jsonl, parse_jsonl_line


def test_parse_jsonl_line_valid() -> None:
    data = {
        "timestamp": "2026-10-22T12:00:00+03:00",
        "level": "INFO",
        "source": "app",
        "message": "pupupu",
    }
    line = json.dumps(data, ensure_ascii=False)

    event = parse_jsonl_line(line)

    assert event.timestamp == datetime.fromisoformat(data["timestamp"])
    assert event.level == "INFO"
    assert event.source == "app"
    assert event.message == "pupupu"

def test_parse_jsonl_line_empty() -> None:
    with pytest.raises(json.decoder.JSONDecodeError):
        parse_jsonl_line("")

def test_parse_jsonl_line_invalid() -> None:
    with pytest.raises(json.decoder.JSONDecodeError):
        parse_jsonl_line("eojghhdlajgnad;ngjorg;i")

def test_parse_jsonl_invalid_timestamp(tmp_path: Path) -> None:
    path = tmp_path / "events.jsonl"
    data = {
        "timestamp": "not-a-date",
        "level": "INFO",
        "source": "app",
        "message": "6767",
    }
    path.write_text(json.dumps(data) + "\n", encoding="utf-8")

    with pytest.raises(InvalidTimestampError):
        list(parse_jsonl(str(path), SkippedEvent()))


@pytest.mark.parametrize("broken_line", ['broken', '{"timestamp": "not-a-date"}'])
def test_parse_jsonl_skip_invalid(tmp_path: Path, broken_line: str) -> None:
    path = tmp_path / "events.jsonl"
    data = {
        "timestamp": "2026-10-23T12:00:00+03:00",
        "level": "INFO",
        "source": "app",
        "message": "Start",
    }
    line = json.dumps(data)
    path.write_text(line + "\n" + broken_line + "\n" + line + "\n", encoding="utf-8")
    skipped = SkippedEvent()

    events = list(parse_jsonl(str(path), skipped, skip_invalid=True))

    assert len(events) == 2
    assert all(event.source == "app" for event in events)
    assert skipped.skipped == 1
