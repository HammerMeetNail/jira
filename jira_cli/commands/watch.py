import click
import requests
import sys
import time
from jira_cli.utils.config import get_config

@click.command()
@click.argument('issue_key')
@click.option('--interval', type=int, default=10, help='Polling interval in seconds')
def watch(issue_key, interval):
    """Watch an issue for changes in real-time"""
    config = get_config()
    if not config:
        click.echo("Error: Configuration not found. Please run 'jira-cli configure' first.")
        sys.exit(1)

    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {config["api_token"]}'
    }

    try:
        # Get initial state
        issue_url = f"https://{config['domain']}/rest/api/{config.get('api_version', '2')}/issue/{issue_key}"
        response = requests.get(issue_url, headers=headers)
        
        if response.status_code != 200:
            click.echo(f"Error getting issue: {response.status_code}")
            click.echo(f"Response: {response.text}")
            sys.exit(1)
            
        last_updated = response.json()['fields']['updated']
        click.echo(f"Watching {issue_key}. Last updated: {last_updated}")
        
        while True:
            time.sleep(interval)
            
            response = requests.get(issue_url, headers=headers)
            if response.status_code != 200:
                click.echo(f"Error getting issue: {response.status_code}")
                click.echo(f"Response: {response.text}")
                continue
                
            current_updated = response.json()['fields']['updated']
            if current_updated != last_updated:
                last_updated = current_updated
                click.echo(f"\nIssue updated: {current_updated}")
                # Show what changed
                click.echo("Changes:")
                # TODO: Implement diff functionality
                click.echo("Use 'jira-cli get' to see full details")
                
    except requests.exceptions.RequestException as e:
        click.echo(f"Error watching issue: {e}")
        if hasattr(e, 'response'):
            click.echo(f"Status code: {e.response.status_code}")
            click.echo(f"Response content: {e.response.text[:500]}")
        sys.exit(1)
    except KeyboardInterrupt:
        click.echo("\nStopped watching issue")
        sys.exit(0)
