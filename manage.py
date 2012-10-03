#!/usr/bin/env python
import os

from django.core.management import execute_manager

from programtracker import settings #settings

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "programtracker.settings")
    execute_manager(settings)
