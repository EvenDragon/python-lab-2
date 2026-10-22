from pathlib import Path

from typer.testing import CliRunner

from streamstats.__main__ import app

runner = CliRunner()

def test_jsonl_parser() -> None:
    path = Path(__file__).parent / "test_files" / "events_test_1.jsonl"

    result = runner.invoke(app, [str(path), "--format", "jsonl"])

    assert result.exit_code == 0
    assert result.stdout == "3\n"
