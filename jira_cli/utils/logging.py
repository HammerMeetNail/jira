import click
import json
from typing import Any

class Logger:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def log_request(self, method: str, url: str, headers: dict, data: Any = None):
        if not self.verbose:
            return
            
        click.echo("\n--- REQUEST ---")
        click.echo(f"{method} {url}")
        click.echo("Headers:")
        click.echo(json.dumps(headers, indent=2))
        if data:
            click.echo("Body:")
            click.echo(json.dumps(data, indent=2))

    def log_response(self, status_code: int, headers: dict, data: Any = None):
        if not self.verbose:
            return
            
        click.echo("\n--- RESPONSE ---")
        click.echo(f"Status: {status_code}")
        click.echo("Headers:")
        click.echo(json.dumps(dict(headers), indent=2))
        if data:
            click.echo("Body:")
            click.echo(json.dumps(data, indent=2))

    def log_info(self, message: str):
        if self.verbose:
            click.echo(f"[INFO] {message}")

    def log_error(self, message: str):
        click.echo(f"[ERROR] {message}", err=True)

logger = Logger()
