# Jira CLI

> This repository was created by DeepSeek-V3

A command line interface for managing Jira issues.

## Installation

1. Install the package:
```bash
pip install .
```

2. Configure your credentials:
```bash
jira-cli configure
```

## Current Features

### Issue Management
- Create issues
- Get issue details
- Update issues
- Delete issues
- Add comments
- Manage attachments
- Transition issues through workflows

### Search & Monitoring
- Search issues with JQL
- Watch/unwatch issues
- Dashboard for recent activity

### Configuration
- Interactive configuration setup
- Environment variable support
- Multiple project support

## Usage Examples

### Create an Issue
```bash
jira-cli create \
  --project PROJECT_KEY \
  --summary "Issue Summary" \
  --type "Issue Type" \
  [--description "Description"] \
  [--fields '{"field": "value"}']
```

### Examples

1. Create a basic task:
```bash
jira-cli create --project ABC --summary "Fix login bug" --type "Task"
```

2. Create an issue with description and custom fields:
```bash
jira-cli create --project ABC --summary "New feature" --type "Story" \
  --description "Implement new search functionality" \
  --fields '{"priority": {"name": "High"}}'
```

## Configuration

The CLI stores your credentials in `~/.jira_cli_config`. You can either:
- Run `jira-cli configure` to set up credentials interactively
- Set environment variables:
  ```bash
  export JIRA_DOMAIN="your-domain.atlassian.net"
  export JIRA_API_TOKEN="your_api_token"
  ```

## Planned Changes

1. **Authentication Improvements**
- OAuth authentication support
- Token refresh functionality
- Session timeout handling

2. **Dashboard Enhancements**
- Filtering by issue type
- Charts/graphs for visual representation
- Custom fields in dashboard view
- Pagination for large result sets

3. **Configuration Management**
- Multiple Jira instances support
- Configuration profiles
- Configuration validation

4. **Error Handling**
- Improved error messages
- Retry logic for failed requests
- Better rate limiting handling

5. **Output Formatting**
- JSON/CSV output formats
- Color-coded status indicators
- Table formatting options

6. **Integration Features**
- Webhook support
- CI/CD tool integration
- Jira Service Management support

7. **Performance Improvements**
- Caching for frequently accessed data
- Parallel request handling
- Optimized API call patterns

8. **Documentation**
- Comprehensive CLI help
- Man pages for each command
- Common workflow examples

9. **Testing**
- Unit tests for all commands
- Integration tests
- CI/CD pipeline for testing

10. **Security**
- Secure credential storage
- Audit logging
- Role-based access control

## Requirements
- Python 3.7+
- Click
- Requests
