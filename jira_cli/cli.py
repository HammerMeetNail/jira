import click
from jira_cli.commands import configure, create, get, update, delete, comment, watch, dashboard, attachment, search, transition
from jira_cli.utils.logging import Logger, logger

@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
def cli(verbose):
    """Jira CLI - Command line interface for Jira"""
    logger.verbose = verbose

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
