import click
import requests
import sys
from jira_cli.utils.config import get_config

@click.command()
@click.argument('issue_key')
@click.option('--comment', required=True, help='Comment text to add')
@click.option('--visibility', help='Comment visibility (role or group)')
def comment(issue_key, comment, visibility):
    """Add a comment to a Jira issue"""
    config = get_config()
    if not config:
        click.echo("Error: Configuration not found. Please run 'jira-cli configure' first.")
        sys.exit(1)

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {config["api_token"]}'
    }

    comment_data = {
        'body': comment
    }

    if visibility:
        comment_data['visibility'] = {
            'type': 'role' if visibility.startswith('role:') else 'group',
            'value': visibility.split(':')[1]
        }

    try:
        api_url = f"https://{config['domain']}/rest/api/{config.get('api_version', '2')}/issue/{issue_key}/comment"
        response = requests.post(
            api_url,
            headers=headers,
            json=comment_data
        )
        
        if response.status_code == 201:
            comment = response.json()
            click.echo(f"Comment added successfully to {issue_key}!")
            click.echo(f"Comment ID: {comment['id']}")
        else:
            click.echo(f"Error adding comment: {response.status_code}")
            click.echo(f"Response: {response.text}")
            sys.exit(1)
            
    except requests.exceptions.RequestException as e:
        click.echo(f"Error adding comment: {e}")
        if hasattr(e, 'response'):
            click.echo(f"Status code: {e.response.status_code}")
            click.echo(f"Response content: {e.response.text[:500]}")
        sys.exit(1)
