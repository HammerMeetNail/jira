import click
from jira_cli.commands import create, configure, get, update, comment, transition, attachment, search, watch, dashboard, delete

@click.group()
def cli():
    """Jira CLI tool for managing issues"""
    pass

cli.add_command(create)
cli.add_command(configure)
cli.add_command(get)
cli.add_command(update)
cli.add_command(comment)
cli.add_command(transition)
cli.add_command(attachment)
cli.add_command(search)
cli.add_command(watch)
cli.add_command(dashboard)
cli.add_command(delete)
