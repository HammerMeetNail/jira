import click
import requests
import sys
from jira_cli.utils.config import get_config

@click.command()
@click.argument('issue_key')
def delete(issue_key):
    """Delete a Jira issue"""
    config = get_config()
    if not config:
        click.echo("Error: Configuration not found. Please run 'jira-cli configure' first.")
        sys.exit(1)

    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {config["api_token"]}'
    }

    try:
        api_url = f"https://{config['domain']}/rest/api/{config.get('api_version', '2')}/issue/{issue_key}"
        
        # First confirm deletion
        if not click.confirm(f"Are you sure you want to delete issue {issue_key}? This cannot be undone."):
            click.echo("Deletion cancelled")
            return
            
        response = requests.delete(
            api_url,
            headers=headers
        )
        
        if response.status_code == 204:
            click.echo(f"Issue {issue_key} deleted successfully")
        else:
            click.echo(f"Error deleting issue: {response.status_code}")
            click.echo(f"Response: {response.text}")
            sys.exit(1)
            
    except requests.exceptions.RequestException as e:
        click.echo(f"Error deleting issue: {e}")
        if hasattr(e, 'response'):
            click.echo(f"Status code: {e.response.status_code}")
            click.echo(f"Response content: {e.response.text[:500]}")
        sys.exit(1)
