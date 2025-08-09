import typer, json
from rich import print
from .pipeline import run_once
from .utils.logging import setup_logging

app = typer.Typer(no_args_is_help=True)

@app.command()
def run(sources: str = "gets,trademe"):
    setup_logging()
    names = [s.strip() for s in sources.split(",") if s.strip()]
    paths = run_once(tuple(names))
    print("[bold green]Done.[/bold green] Outputs:")
    print(json.dumps(paths, indent=2))

if __name__ == "__main__":
    app()
