import click
import requests
import sys
from jira_cli.utils.config import get_config
from datetime import datetime, timedelta

@click.command()
@click.option('--projects', help='Comma-separated list of project keys')
@click.option('--days', type=int, default=7, help='Number of days to look back')
def dashboard(projects, days):
    """Show a dashboard of recent activity across projects"""
    config = get_config()
    if not config:
        click.echo("Error: Configuration not found. Please run 'jira-cli configure' first.")
        sys.exit(1)

    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {config["api_token"]}'
    }

    try:
        # Build JQL query
        jql_parts = []
        if projects:
            jql_parts.append(f"project in ({projects})")
        jql_parts.append(f"updated >= -{days}d")
        jql = " AND ".join(jql_parts)

        search_url = f"https://{config['domain']}/rest/api/{config.get('api_version', '2')}/search"
        params = {
            'jql': jql,
            'maxResults': 100,
            'fields': 'key,summary,status,updated,assignee'
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
                click.echo("No recent activity found")
                return
                
            # Group by project
            projects = {}
            for issue in issues:
                project_key = issue['key'].split('-')[0]
                if project_key not in projects:
                    projects[project_key] = []
                projects[project_key].append(issue)
            
            # Display dashboard
            for project, issues in projects.items():
                click.echo(f"\nProject: {project}")
                click.echo("=" * (len(project) + 9))
                for issue in issues:
                    key = issue['key']
                    summary = issue['fields']['summary']
                    status = issue['fields']['status']['name']
                    updated = issue['fields']['updated']
                    assignee = issue['fields']['assignee']['displayName'] if issue['fields']['assignee'] else 'Unassigned'
                    click.echo(f"{key}: {status} - {summary}")
                    click.echo(f"  Updated: {updated} | Assignee: {assignee}")
                    
        else:
            click.echo(f"Error getting dashboard data: {response.status_code}")
            click.echo(f"Response: {response.text}")
            sys.exit(1)
            
    except requests.exceptions.RequestException as e:
        click.echo(f"Error getting dashboard data: {e}")
        if hasattr(e, 'response'):
            click.echo(f"Status code: {e.response.status_code}")
            click.echo(f"Response content: {e.response.text[:500]}")
        sys.exit(1)
