import click
import json
from jira_cli.utils.api import create_issue
from jira_cli.utils.validators import validate_fields
from jira_cli.utils.config import get_config

@click.command(name='create')
@click.option('--project', required=True, help='Project key')
@click.option('--summary', required=True, help='Issue summary')
@click.option('--description', help='Issue description')
@click.option('--type', 'issuetype', required=True, help='Issue type name')
@click.option('--fields', help='Additional fields as JSON string')
def create_command(project, summary, description, issuetype, fields):
    """Create a new Jira issue"""
    config = get_config()
    
    try:
        # Validate and parse additional fields
        additional_fields = {}
        if fields:
            additional_fields = validate_fields(fields)
        
        # Create the issue
        issue = create_issue(
            config,
            project=project,
            summary=summary,
            description=description,
            issuetype=issuetype,
            fields=additional_fields
        )
        
        click.echo(f"Issue created successfully: {issue['key']}")
        click.echo(f"URL: {config['domain']}/browse/{issue['key']}")
        
    except Exception as e:
        click.echo(f"Error creating issue: {str(e)}", err=True)
        raise click.Abort()

# Expose the command function
create = create_command
