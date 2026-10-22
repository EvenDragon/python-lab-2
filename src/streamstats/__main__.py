import typer

app = typer.Typer()

@app.command(context_settings={"ignore_unknown_options": True})
def analyze(input: str) -> None:
    """Analyze file and make report of it"""
    typer.echo(input)

if __name__ == "__main__":
    app()
