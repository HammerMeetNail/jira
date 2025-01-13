import os
import json
from typing import Dict
import click
from pathlib import Path

CONFIG_FILE = Path.home() / ".jira_cli_config"

def get_config() -> Dict:
    """Get Jira configuration from environment or config file"""
    config = {
        'domain': os.getenv('JIRA_DOMAIN'),
        'api_token': os.getenv('JIRA_API_TOKEN'),
        'api_version': os.getenv('JIRA_API_VERSION', '2')  # Default to v2
    }
    
    if not all(config.values()):
        # Try to load from config file
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE) as f:
                config.update(json.load(f))
    
    if not all(config.values()):
        click.echo("Error: Missing configuration. Please set JIRA_DOMAIN and JIRA_API_TOKEN", err=True)
        click.echo("You can set these as environment variables or run 'jira-cli configure'", err=True)
        raise click.Abort()
    
    return config

def save_config(domain: str, api_token: str, api_version: str = '2'):
    """Save configuration to file"""
    config = {
        'domain': domain,
        'api_token': api_token,
        'api_version': api_version
    }
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)
    click.echo(f"Configuration saved to {CONFIG_FILE}")
