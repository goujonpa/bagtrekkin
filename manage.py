#!/usr/bin/env python
import os
import sys

if not os.environ.get('ENV', None):
    import dotenv

if __name__ == "__main__":
    try:
        dotenv.read_dotenv()
    except Exception:
        pass
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bagtrekkin.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
