"""
djangorave default settings are defined here and determined in combination
with what has been defined in django.conf.settings.
"""

# stdlib import

# django imports
from django.conf import settings

# 3rd party imports

# project imports

SANDBOX = settings.get("SANDBOX", True)

if SANDBOX:
    PUBLIC_KEY = settings.get("SANDBOX_PUBLIC_KEY", "not set")
else:
    PUBLIC_KEY = settings.get("PRODUCTION_PUBLIC_KEY", "not set")
