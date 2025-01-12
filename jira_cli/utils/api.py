import requests
from typing import Dict, Any
from jira_cli.utils.config import get_config

def create_issue(config: Dict[str, str], project: str, summary: str, 
                issuetype: str, description: str = None, fields: Dict = None) -> Dict[str, Any]:
    """Create a new Jira issue"""
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {config["api_token"]}'
    }

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

    try:
        response = requests.post(
            f"https://{config['domain']}/rest/api/{config.get('api_version', '2')}/issue/",
            headers=headers,
            json=issue_data
        )
        
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.RequestException as e:
        error_msg = f"API Error: {str(e)}"
        if hasattr(e, 'response'):
            error_msg += f"\nStatus Code: {e.response.status_code}"
            if e.response.text:
                error_msg += f"\nResponse: {e.response.text[:500]}"
        raise Exception(error_msg)
