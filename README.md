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

### Verbose Logging
- Detailed logging of all API requests and responses
- Logs include:
  - Request method and URL
  - Request headers
  - Request payload (if applicable)
  - Response status code
  - Response headers
  - Response body (truncated if large)
- Enable verbose mode by adding the `--verbose` flag before the command:
  ```bash
  jira-cli --verbose [command]
  ```

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

The CLI uses a configuration file located at `~/.jira_cli_config` to store settings. Here's how to set it up:

1. **Interactive Setup**
   Run the configuration wizard:
   ```bash
   jira-cli configure
   ```
   This will prompt for:
   - Jira domain (e.g., your-domain.atlassian.net)
   - API token
   - API version (defaults to 2)

2. **Environment Variables**
   Alternatively, you can configure using environment variables:
   ```bash
   export JIRA_DOMAIN="your-domain.atlassian.net"
   export JIRA_API_TOKEN="your_api_token"
   export JIRA_API_VERSION="2"  # Optional, defaults to 2
   ```

3. **Configuration File**
   The configuration is stored in `~/.jira_cli_config` with this format:
   ```json
   {
     "domain": "your-domain.atlassian.net",
     "api_token": "your_api_token",
     "api_version": "2"
   }
   ```

4. **Example Setup**
   Here's a complete example using environment variables:
   ```bash
   export JIRA_DOMAIN="mycompany.atlassian.net"
   export JIRA_API_TOKEN="abc123xyz456"
   export JIRA_API_VERSION="3"  # For Jira Cloud API v3
   ```

The CLI will automatically use the updated configuration on the next command execution.

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

## Quick Start

1. Install the CLI:
```bash
pip install .
```

2. Configure your Jira credentials:
```bash
jira-cli configure
```

3. Start using the CLI:
```bash
jira-cli create --project ABC --summary "New Issue" --type "Task"
```

## Command Reference

### Core Commands
- `create`: Create new issues
- `get`: Get issue details
- `update`: Modify existing issues
- `delete`: Remove issues
- `comment`: Manage issue comments
- `transition`: Move issues through workflows

#### Transition Command Usage

List available transitions for an issue:
```bash
jira-cli transition ISSUE-KEY --list
```

Execute a transition using either the transition ID or name:
```bash
# Using transition ID
jira-cli transition ISSUE-KEY --transition TRANSITION_ID

# Using transition name
jira-cli transition ISSUE-KEY --transition "Transition Name"
```

Add a comment during transition:
```bash
jira-cli transition ISSUE-KEY --transition "Transition Name" --comment "Your comment here"
```

### Advanced Commands
- `search`: Find issues using JQL
- `watch`: Manage issue watchers
- `dashboard`: View recent activity
- `configure`: Manage CLI settings
- `attachment`: Handle issue attachments

## Troubleshooting

### Common Issues

1. **Authentication Errors**
- Verify your API token is valid
- Check your JIRA_DOMAIN is correct
- Ensure your token has necessary permissions

2. **API Version Mismatch**
- Check your Jira instance version
- Verify configured API version matches
- Update configuration if needed

3. **Rate Limiting**
- Implement retry logic in your scripts
- Use bulk operations when possible
- Consider implementing caching

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request
4. Include tests for new features
5. Update documentation as needed

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
