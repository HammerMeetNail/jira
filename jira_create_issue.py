import os
import sys
import argparse
import json
import requests

def main():
    # Get environment variables
    JIRA_DOMAIN = os.getenv('JIRA_DOMAIN')
    JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')

    if not all([JIRA_DOMAIN, JIRA_API_TOKEN]):
        print("Error: Please set JIRA_DOMAIN and JIRA_API_TOKEN environment variables")
        sys.exit(1)

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Create a Jira issue')
    parser.add_argument('--project', required=True, help='Project key')
    parser.add_argument('--summary', required=True, help='Issue summary')
    parser.add_argument('--description', help='Issue description')
    parser.add_argument('--issuetype', required=True, help='Issue type name')
    parser.add_argument('--fields', type=json.loads, help='Additional fields as JSON string')
    args = parser.parse_args()

    # Set up headers with Bearer token
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {JIRA_API_TOKEN}'
    }

    # Build issue data
    issue_data = {
        "fields": {
            "project": {
                "key": args.project
            },
            "summary": args.summary,
            "issuetype": {
                "name": args.issuetype
            }
        }
    }

    # Add description if provided
    if args.description:
        issue_data["fields"]["description"] = args.description

    # Add additional fields if provided
    if args.fields:
        issue_data["fields"].update(args.fields)

    # Make request to create issue
    try:
        api_url = f"https://{JIRA_DOMAIN}/rest/api/2/issue/"
        print(f"Creating issue in project: {args.project}")
        
        response = requests.post(
            api_url,
            headers=headers,
            json=issue_data
        )
        
        if response.status_code == 201:
            issue = response.json()
            print(f"Issue created successfully!")
            print(f"Key: {issue['key']}")
            print(f"URL: https://{JIRA_DOMAIN}/browse/{issue['key']}")
        else:
            print(f"Error creating issue: {response.status_code}")
            print(f"Response: {response.text}")
            sys.exit(1)
            
    except requests.exceptions.RequestException as e:
        print(f"Error creating issue: {e}")
        if hasattr(e, 'response'):
            print(f"Status code: {e.response.status_code}")
            print(f"Response content: {e.response.text[:500]}")
        sys.exit(1)

if __name__ == "__main__":
    main()
