import json
from datetime import datetime
from pathlib import Path

import pytest

from streamstats.errors import InvalidTimestampError
from streamstats.parsers import parse_jsonl, parse_jsonl_line


def test_parse_jsonl_line_valid():
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

def test_parse_jsonl_line_empty():
    with pytest.raises(json.decoder.JSONDecodeError):
        parse_jsonl_line("")

def test_parse_jsonl_line_invalid():
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
        list(parse_jsonl(str(path)))
