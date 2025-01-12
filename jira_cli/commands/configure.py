import click
from jira_cli.utils.config import save_config

@click.command()
def configure():
    """Configure Jira credentials and API settings"""
    domain = click.prompt("Enter your Jira domain (e.g., your-domain.atlassian.net)")
    api_token = click.prompt("Enter your Jira API token", hide_input=True)
    api_version = click.prompt(
        "Enter API version (default: 2)", 
        default="2",
        show_default=True
    )
    
    save_config(domain, api_token, api_version)
    click.echo("Configuration saved successfully!")
