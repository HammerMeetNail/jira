import click
import requests
import sys
from jira_cli.utils.config import get_config
from jira_cli.utils.logging import logger

@click.command()
@click.argument('issue_key')
@click.option('--transition', required=True, help='Transition ID or name')
@click.option('--comment', help='Comment to add with the transition')
def transition(issue_key, transition, comment):
    """Transition a Jira issue through its workflow"""
    config = get_config()
    if not config:
        click.echo("Error: Configuration not found. Please run 'jira-cli configure' first.")
        sys.exit(1)

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {config["api_token"]}'
    }

    # First get available transitions
    try:
        transitions_url = f"https://{config['domain']}/rest/api/{config.get('api_version', '2')}/issue/{issue_key}/transitions"
        # Log request details
        logger.log_request(
            method='GET',
            url=transitions_url,
            headers=headers
        )
        
        response = requests.get(transitions_url, headers=headers)
        
        # Log response details
        logger.log_response(
            status_code=response.status_code,
            headers=response.headers,
            data=response.json() if response.content else None
        )
        
        if response.status_code != 200:
            click.echo(f"Error getting transitions: {response.status_code}")
            click.echo(f"Response: {response.text}")
            sys.exit(1)
            
        transitions = response.json()['transitions']
        transition_id = None
        
        # Try to match by ID or name
        for t in transitions:
            if str(t['id']) == transition or t['name'].lower() == transition.lower():
                transition_id = t['id']
                break
                
        if not transition_id:
            click.echo(f"Error: Transition '{transition}' not found. Available transitions:")
            for t in transitions:
                click.echo(f"  {t['id']}: {t['name']}")
            sys.exit(1)
            
        # Build transition data
        transition_data = {
            'transition': {
                'id': transition_id
            }
        }
        
        if comment:
            transition_data['update'] = {
                'comment': [{
                    'add': {
                        'body': comment
                    }
                }]
            }

        # Execute transition
        transition_url = f"https://{config['domain']}/rest/api/{config.get('api_version', '2')}/issue/{issue_key}/transitions"
        # Log request details
        logger.log_request(
            method='POST',
            url=transition_url,
            headers=headers,
            data=transition_data
        )
        
        response = requests.post(
            transition_url,
            headers=headers,
            json=transition_data
        )
        
        # Log response details
        logger.log_response(
            status_code=response.status_code,
            headers=response.headers,
            data=response.text if response.content else None
        )
        
        if response.status_code == 204:
            click.echo(f"Issue {issue_key} transitioned successfully!")
        else:
            click.echo(f"Error transitioning issue: {response.status_code}")
            click.echo(f"Response: {response.text}")
            sys.exit(1)
            
    except requests.exceptions.RequestException as e:
        click.echo(f"Error transitioning issue: {e}")
        if hasattr(e, 'response'):
            click.echo(f"Status code: {e.response.status_code}")
            click.echo(f"Response content: {e.response.text[:500]}")
        sys.exit(1)
