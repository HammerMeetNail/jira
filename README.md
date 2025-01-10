# Jira API Scripts

This repository contains Python scripts for interacting with Jira's REST API.

## Scripts

### jira_get_issue.py
Fetches details of a specific Jira issue.

#### Usage:
```bash
python3 jira_get_issue.py ISSUE_KEY
```

#### Output:
- Issue key
- Summary
- Status
- Description (if available)

### jira_create_issue.py
Creates a new Jira issue with customizable fields.

#### Usage:
```bash
python3 jira_create_issue.py --project PROJECT_KEY --summary "Issue Summary" --issuetype "Issue Type" [--description "Description"] [--fields '{"field": "value"}']
```

#### Examples:
1. Create a basic issue:
```bash
python3 jira_create_issue.py --project PROJECT --summary "Test Issue" --issuetype "Task"
```

#### Output:
- Issue key
- Issue URL

## Setup

1. Set environment variables:
```bash
export JIRA_DOMAIN="issues.example.com"
export JIRA_API_TOKEN="your_personal_access_token"
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Requirements
- Python 3.x
- requests library
- Valid Jira API token with appropriate permissions
