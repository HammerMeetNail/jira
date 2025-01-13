import click
import requests
import os
import sys
from jira_cli.utils.config import get_config

@click.command()
@click.argument('issue_key')
def get(issue_key):
    """Get details of a Jira issue"""
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
        response = requests.get(api_url, headers=headers)
        
        if response.status_code == 200:
            issue = response.json()
            click.echo(f"Issue: {issue['key']}")
            click.echo(f"Summary: {issue['fields']['summary']}")
            click.echo(f"Description: {issue['fields']['description']}")
            click.echo(f"Status: {issue['fields']['status']['name']}")
            click.echo(f"Priority: {issue['fields']['priority']['name'] if issue['fields']['priority'] else 'None'}")
            click.echo(f"Assignee: {issue['fields']['assignee']['displayName'] if issue['fields']['assignee'] else 'Unassigned'}")
            click.echo(f"Reporter: {issue['fields']['reporter']['displayName'] if issue['fields']['reporter'] else 'None'}")
            click.echo(f"Watchers: {issue['fields']['watches']['watchCount']}")
            if issue['fields'].get('watchers'):
                click.echo(f"Watchers List: {', '.join([w['displayName'] for w in issue['fields']['watchers']])}")
            click.echo(f"Labels: {', '.join(issue['fields']['labels']) if issue['fields']['labels'] else 'None'}")
            click.echo(f"URL: https://{config['domain']}/browse/{issue['key']}")
        else:
            click.echo(f"Error getting issue: {response.status_code}")
            click.echo(f"Response: {response.text}")
            sys.exit(1)
            
    except requests.exceptions.RequestException as e:
        click.echo(f"Error getting issue: {e}")
        if hasattr(e, 'response'):
            click.echo(f"Status code: {e.response.status_code}")
            click.echo(f"Response content: {e.response.text[:500]}")
        sys.exit(1)
