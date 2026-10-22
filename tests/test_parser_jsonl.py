import json
from datetime import datetime

import pytest

from streamstats.parsers import parse_jsonl_line


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
