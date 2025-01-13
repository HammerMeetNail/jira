import requests
from typing import Dict, Any
from jira_cli.utils.config import get_config
from jira_cli.utils.logging import logger

def make_request(method, endpoint, headers=None, data=None):
    """Make a generic API request with logging"""
    config = get_config()
    if not config:
        raise Exception("Configuration not found. Please run 'jira-cli configure' first.")

    api_url = f"https://{config['domain']}/rest/api/{config.get('api_version', '2')}/{endpoint}"
    headers = headers or {}
    headers.update({
        'Accept': 'application/json',
        'Authorization': f'Bearer {config["api_token"]}'
    })

    logger.log_request(method, api_url, headers, data)
    
    try:
        response = requests.request(
            method,
            api_url,
            headers=headers,
            json=data
        )
        logger.log_response(response.status_code, response.headers, response.json())
        return response
    except requests.exceptions.RequestException as e:
        logger.log_error(f"API Error: {str(e)}")
        if hasattr(e, 'response'):
            logger.log_error(f"Status Code: {e.response.status_code}")
            if e.response.text:
                logger.log_error(f"Response: {e.response.text[:500]}")
        raise e

def create_issue(config: Dict[str, str], project: str, summary: str, 
                issuetype: str, description: str = None, fields: Dict = None) -> Dict[str, Any]:
    """Create a new Jira issue"""
    issue_data = {
        "fields": {
            "project": {
                "key": project
            },
            "summary": summary,
            "issuetype": {
                "name": issuetype
            }
        }
    }

    if description:
        issue_data["fields"]["description"] = description

    if fields:
        issue_data["fields"].update(fields)

    response = make_request(
        'POST',
        'issue/',
        headers={
            'Content-Type': 'application/json'
        },
        data=issue_data
    )
    
    response.raise_for_status()
    return response.json()
