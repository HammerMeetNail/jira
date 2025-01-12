import click
import requests
import sys
from jira_cli.utils.config import get_config

@click.command()
@click.argument('issue_key')
@click.option('--summary', help='Update issue summary')
@click.option('--description', help='Update issue description')
@click.option('--fields', help='Additional fields as JSON string')
def update(issue_key, summary, description, fields):
    """Update an existing Jira issue"""
    config = get_config()
    if not config:
        click.echo("Error: Configuration not found. Please run 'jira-cli configure' first.")
        sys.exit(1)

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {config["api_token"]}'
    }

    update_data = {}
    if summary:
        update_data['summary'] = summary
    if description:
        update_data['description'] = description
    if fields:
        try:
            import json
            update_data.update(json.loads(fields))
        except json.JSONDecodeError:
            click.echo("Error: Invalid JSON in --fields parameter")
            sys.exit(1)

    if not update_data:
        click.echo("Error: No update data provided")
        sys.exit(1)

    try:
        api_url = f"https://{config['domain']}/rest/api/{config.get('api_version', '2')}/issue/{issue_key}"
        response = requests.put(
            api_url,
            headers=headers,
            json={'fields': update_data}
        )
        
        if response.status_code == 204:
            click.echo(f"Issue {issue_key} updated successfully!")
        else:
            click.echo(f"Error updating issue: {response.status_code}")
            click.echo(f"Response: {response.text}")
            sys.exit(1)
            
    except requests.exceptions.RequestException as e:
        click.echo(f"Error updating issue: {e}")
        if hasattr(e, 'response'):
            click.echo(f"Status code: {e.response.status_code}")
            click.echo(f"Response content: {e.response.text[:500]}")
        sys.exit(1)
