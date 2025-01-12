import click
import requests
import sys
from pathlib import Path
from jira_cli.utils.config import get_config

@click.command()
@click.argument('issue_key')
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--comment', help='Comment to add with the attachment')
def attachment(issue_key, file_path, comment):
    """Attach a file to a Jira issue"""
    config = get_config()
    if not config:
        click.echo("Error: Configuration not found. Please run 'jira-cli configure' first.")
        sys.exit(1)

    headers = {
        'Accept': 'application/json',
        'X-Atlassian-Token': 'no-check',
        'Authorization': f'Bearer {config["api_token"]}'
    }

    try:
        file_path = Path(file_path)
        attachment_url = f"https://{config['domain']}/rest/api/{config.get('api_version', '2')}/issue/{issue_key}/attachments"
        
        with open(file_path, 'rb') as file:
            files = {'file': (file_path.name, file)}
            response = requests.post(
                attachment_url,
                headers=headers,
                files=files
            )
            
        if response.status_code == 200:
            click.echo(f"File attached successfully to {issue_key}!")
            if comment:
                # Add comment if provided
                comment_url = f"https://{config['domain']}/rest/api/{config.get('api_version', '2')}/issue/{issue_key}/comment"
                comment_data = {
                    'body': comment
                }
                response = requests.post(
                    comment_url,
                    headers=headers,
                    json=comment_data
                )
                if response.status_code == 201:
                    click.echo("Comment added successfully!")
                else:
                    click.echo(f"Error adding comment: {response.status_code}")
                    click.echo(f"Response: {response.text}")
        else:
            click.echo(f"Error attaching file: {response.status_code}")
            click.echo(f"Response: {response.text}")
            sys.exit(1)
            
    except requests.exceptions.RequestException as e:
        click.echo(f"Error attaching file: {e}")
        if hasattr(e, 'response'):
            click.echo(f"Status code: {e.response.status_code}")
            click.echo(f"Response content: {e.response.text[:500]}")
        sys.exit(1)
