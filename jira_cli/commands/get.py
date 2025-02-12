import click
import sys
from jira_cli.utils.api import make_request
from jira_cli.utils.config import get_config
from jira_cli.utils.logging import logger

@click.command()
@click.argument('issue_key')
def get(issue_key):
    """Get details of a Jira issue"""
    config = get_config()
    if not config:
        click.echo("Error: Configuration not found. Please run 'jira-cli configure' first.")
        sys.exit(1)

    try:
        logger.log_info(f"Getting issue {issue_key}")
        
        response = make_request(
            'GET',
            f'issue/{issue_key}',
            headers={
                'Accept': 'application/json'
            }
        )
        
        if response.status_code == 200:
            issue = response.json()
            logger.log_info(f"Successfully retrieved issue {issue_key}")
            
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
            logger.log_error(f"Error getting issue: {response.status_code}")
            click.echo(f"Error getting issue: {response.status_code}")
            click.echo(f"Response: {response.text}")
            sys.exit(1)
            
    except Exception as e:
        logger.log_error(f"Error getting issue: {str(e)}")
        click.echo(f"Error getting issue: {e}")
        sys.exit(1)
