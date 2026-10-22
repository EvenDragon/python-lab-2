from typing import Annotated

import typer

from streamstats.analysis import count_events
from streamstats.parsers import parse_jsonl

app = typer.Typer()

@app.command()
def analyze(
        input: Annotated[str, typer.Argument()],
        format: Annotated[str,typer.Option("--format")],
        output: Annotated[str, typer.Option("--output")] = "report.json",
        skip_invalid: Annotated[bool, typer.Option("--skip-invalid")] = False
        ) -> None:
    """Analyze file and make report of it"""
    counts = count_events(parse_jsonl(input, skip_invalid))
    typer.echo(counts.total())

if __name__ == "__main__":
    app()
