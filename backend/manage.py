#!/usr/bin/env python
"""Django entrypoint — is script se `runserver`, `migrate`, etc. chalate hain."""
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django install nahi mila. `pip install -r requirements.txt` chalao."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
