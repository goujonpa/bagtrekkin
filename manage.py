#!/usr/bin/env python
import os
import sys

try:
    import dotenv
    dotenv.read_dotenv()
except ImportError:
    pass

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bagtrekkin.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
