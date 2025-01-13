import click
import json
from jira_cli.utils.api import create_issue
from jira_cli.utils.validators import validate_fields
from jira_cli.utils.config import get_config
from jira_cli.utils.logging import logger

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
        
        logger.log_info(f"Creating issue in project {project}")
        
        # Log request details
        logger.log_request(
            method='POST',
            url=f"{config['domain']}/rest/api/2/issue/",
            headers={
                'Authorization': f"Bearer {config['api_token']}",
                'Content-Type': 'application/json'
            },
            data={
                'project': project,
                'summary': summary,
                'description': description,
                'issuetype': issuetype,
                'fields': additional_fields
            }
        )
        
        # Create the issue
        issue = create_issue(
            config,
            project=project,
            summary=summary,
            description=description,
            issuetype=issuetype,
            fields=additional_fields
        )
        
        # Log response details
        logger.log_response(
            status_code=201,
            headers={'Content-Type': 'application/json'},
            data=issue
        )
        
        click.echo(f"Issue created successfully: {issue['key']}")
        click.echo(f"URL: {config['domain']}/browse/{issue['key']}")
        
    except Exception as e:
        logger.log_error(f"Error creating issue: {str(e)}")
        raise click.Abort()

# Expose the command function
create = create_command
