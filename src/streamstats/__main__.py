from typing import Annotated

import typer

from streamstats.analysis import analyze_events
from streamstats.errors import StreamStatsError
from streamstats.models import SkippedEvent
from streamstats.parsers import parse_files
from streamstats.report import make_report

app = typer.Typer()

@app.command()
def analyze(
        input: Annotated[list[str], typer.Argument()],
        format: Annotated[str,typer.Option("--format")],
        output: Annotated[str, typer.Option("--output")] = "report.json",
        skip_invalid: Annotated[bool, typer.Option("--skip-invalid")] = False
        ) -> None:
    """Analyze file and make report of it"""
    try:
        skipped = SkippedEvent()
        counts = parse_files(input, format, skipped, skip_invalid)
        args = analyze_events(counts)
        args["skipped_lines"] = skipped.skipped
        make_report(args, output)
    except (StreamStatsError, OSError) as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(2) from e
    typer.echo(f"Report saved in: {output}")

@app.callback()
def main() -> None:
    """Stream events from files and generate a statistics report."""


if __name__ == "__main__":
    app()
