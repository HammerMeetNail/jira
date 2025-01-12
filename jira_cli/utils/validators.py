import json
from typing import Dict, Any
import click

def validate_fields(fields_str: str) -> Dict[str, Any]:
    """Validate and parse additional fields JSON string"""
    try:
        fields = json.loads(fields_str)
        if not isinstance(fields, dict):
            raise ValueError("Fields must be a JSON object")
        return fields
    except json.JSONDecodeError as e:
        click.echo(f"Invalid JSON in fields: {str(e)}", err=True)
        raise click.Abort()
    except ValueError as e:
        click.echo(f"Validation error: {str(e)}", err=True)
        raise click.Abort()
