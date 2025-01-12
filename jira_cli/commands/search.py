import click
import requests
import sys
from jira_cli.utils.config import get_config

@click.command()
@click.argument('jql')
@click.option('--max-results', type=int, default=50, help='Maximum number of results to return')
def search(jql, max_results):
    """Search for Jira issues using JQL"""
    config = get_config()
    if not config:
        click.echo("Error: Configuration not found. Please run 'jira-cli configure' first.")
        sys.exit(1)

    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {config["api_token"]}'
    }

    try:
        search_url = f"https://{config['domain']}/rest/api/{config.get('api_version', '2')}/search"
        params = {
            'jql': jql,
            'maxResults': max_results
        }
        
        response = requests.get(
            search_url,
            headers=headers,
            params=params
        )
        
        if response.status_code == 200:
            results = response.json()
            issues = results.get('issues', [])
            
            if not issues:
                click.echo("No issues found matching your query")
                return
                
            for issue in issues:
                key = issue['key']
                summary = issue['fields']['summary']
                status = issue['fields']['status']['name']
                click.echo(f"{key}: {status} - {summary}")
        else:
            click.echo(f"Error searching issues: {response.status_code}")
            click.echo(f"Response: {response.text}")
            sys.exit(1)
            
    except requests.exceptions.RequestException as e:
        click.echo(f"Error searching issues: {e}")
        if hasattr(e, 'response'):
            click.echo(f"Status code: {e.response.status_code}")
            click.echo(f"Response content: {e.response.text[:500]}")
        sys.exit(1)
