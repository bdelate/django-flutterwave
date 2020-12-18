"""
djangorave default settings are defined here and determined in combination
with what has been defined in django.conf.settings.
"""

# stdlib import

# django imports
from django.conf import settings

# 3rd party imports

# project imports

RAVE_SANDBOX = getattr(settings, "RAVE_SANDBOX", True)

if RAVE_SANDBOX:
    PUBLIC_KEY = getattr(settings, "RAVE_SANDBOX_PUBLIC_KEY", "not set")
    SECRET_KEY = getattr(settings, "RAVE_SANDBOX_SECRET_KEY", "not set")
else:
    PUBLIC_KEY = getattr(settings, "RAVE_PRODUCTION_PUBLIC_KEY", "not set")
    SECRET_KEY = getattr(settings, "RAVE_PRODUCTION_SECRET_KEY", "not set")
