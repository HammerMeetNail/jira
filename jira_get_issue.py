import os
import sys
import argparse
import requests

def main():
    # Get environment variables
    JIRA_DOMAIN = os.getenv('JIRA_DOMAIN')
    JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')
    JIRA_API_VERSION = os.getenv('JIRA_API_VERSION', '2')  # Default to version 2 if not specified

    if not all([JIRA_DOMAIN, JIRA_API_TOKEN]):
        print("Error: Please set JIRA_DOMAIN and JIRA_API_TOKEN environment variables")
        sys.exit(1)

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Fetch Jira issue details')
    parser.add_argument('issue_key', help='Jira issue key (e.g. PROJ-123)')
    args = parser.parse_args()

    # Set up headers with Bearer token
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {JIRA_API_TOKEN}'
    }

    # Make request to get issue details
    try:
        api_url = f"https://{JIRA_DOMAIN}/rest/api/{JIRA_API_VERSION}/issue/{args.issue_key}"
        print(f"Making request to: {api_url}")
        
        response = requests.get(
            api_url,
            headers=headers,
            allow_redirects=True  # Follow redirects to capture final response
        )
        print(f"Final URL: {response.url}")
        response.raise_for_status()
        
        try:
            issue = response.json()
            print(f"Issue: {issue['key']}")
            print(f"Summary: {issue['fields']['summary']}")
            print(f"Status: {issue['fields']['status']['name']}")
            print(f"Description: {issue['fields'].get('description', 'No description')}")
        except ValueError as e:
            print("Error parsing JSON response:")
            print(f"Status code: {response.status_code}")
            print(f"Response content: {response.text[:500]}")
            sys.exit(1)
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching issue: {e}")
        if hasattr(e, 'response'):
            print(f"Status code: {e.response.status_code}")
            print(f"Response content: {e.response.text[:500]}")  # Show first 500 chars of response
        sys.exit(1)

if __name__ == "__main__":
    main()
