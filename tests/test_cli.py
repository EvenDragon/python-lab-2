import json
from pathlib import Path

from typer.testing import CliRunner

from streamstats.__main__ import app

runner = CliRunner()

def test_jsonl_parser_empty(tmp_path: Path) -> None:
    input_path = tmp_path / "events.jsonl"
    output_path = tmp_path / "report.json"
    input_path.write_text("", encoding="utf-8")
    result = runner.invoke(app, ["analyze", str(input_path), "--format", "jsonl", "--output", str(output_path)])
    assert result.exit_code == 0, f"{result.output} {result.exception!r}"
    report = json.loads(output_path.read_text(encoding="utf-8"))
    assert report == {
        "total": 0,
        "skipped_lines": 0,
        "by_level": {},
        "by_source": {},
        "first_event": None,
        "last_event": None,
        "top_error_sources": [],
        "top_critical_sources": [],
    }

def test_jsonl_parser(tmp_path: Path) -> None:
    input_path = tmp_path / "events.jsonl"
    output_path = tmp_path / "report.json"

    events = [
        {
            "timestamp": timestamp,
            "level": level,
            "source": source,
            "message": "Тестовое событие",
        }
        for timestamp, level, source in [
            ("2026-10-23T12:02:00+03:00", "ERROR", "db"),
            ("2026-10-23T12:00:00+03:00", "INFO", "app"),
            ("2026-10-23T12:01:00+03:00", "CRITICAL", "api"),
        ]
    ]
    input_path.write_text(
        "\n".join(json.dumps(event, ensure_ascii=False) for event in events),
        encoding="utf-8",
    )


    result = runner.invoke(app, ["analyze", str(input_path), "--format", "jsonl", "--output", str(output_path)])

    assert result.exit_code == 0, f"{result.output} {result.exception!r}"
    report = json.loads(output_path.read_text(encoding="utf-8"))

    assert report == {
        "total": 3,
        "skipped_lines": 0,
        "by_level": {"ERROR": 1, "INFO": 1, "CRITICAL": 1},
        "by_source": {"db": 1, "app": 1, "api": 1},
        "first_event": "2026-10-23T12:00:00+03:00",
        "last_event": "2026-10-23T12:02:00+03:00",
        "top_error_sources": [["db", 1]],
        "top_critical_sources": [["api", 1]],
    }

def test_jsonl_parser_with_invalid_line_and_skip_invalid(tmp_path: Path) -> None:
    input_path = tmp_path / "events.jsonl"
    output_path = tmp_path / "report.json"

    events = [
        {
            "timestamp": timestamp,
            "level": level,
            "source": source,
            "message": "test message",
        }
        for timestamp, level, source in [
            ("2026-10-23T12:02:00+03:00", "ERROR", "db"),
            ("2026-10-dgasgasgggrr:00", "INFargO", "app"),
            ("2026-10-23T12:01:00+03:00", "CRITICAL", "api"),
        ]
    ]
    input_path.write_text(
        "\n".join(json.dumps(event, ensure_ascii=False) for event in events),
        encoding="utf-8",
    )
    result = runner.invoke(app, ["analyze", str(input_path), "--format", "jsonl", "--output", str(output_path),
                           "--skip-invalid"])

    assert result.exit_code == 0, f"{result.output} {result.exception!r}"
    report = json.loads(output_path.read_text(encoding="utf-8"))
    assert report == {
        "total": 2,
        "skipped_lines": 1,
        "by_level": {"ERROR": 1, "CRITICAL": 1},
        "by_source": {"db": 1, "api": 1},
        "first_event": "2026-10-23T12:01:00+03:00",
        "last_event": "2026-10-23T12:02:00+03:00",
        "top_error_sources": [["db", 1]],
        "top_critical_sources": [["api", 1]],
    }
