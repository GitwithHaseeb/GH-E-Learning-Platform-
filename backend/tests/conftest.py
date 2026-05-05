"""Pytest bootstrap — shell mein purana `DJANGO_SETTINGS_MODULE` ho to bhi test settings use hon."""
import os

os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings.test"
