"""
djangoflutterwave default settings are defined here and determined in combination
with what has been defined in django.conf.settings.
"""

# stdlib import

# django imports
from django.conf import settings

# 3rd party imports

# project imports

FLW_SANDBOX = getattr(settings, "FLW_SANDBOX", True)

if FLW_SANDBOX:
    FLW_PUBLIC_KEY = getattr(settings, "FLW_SANDBOX_PUBLIC_KEY", "not set")
    FLW_SECRET_KEY = getattr(settings, "FLW_SANDBOX_SECRET_KEY", "not set")
else:
    FLW_PUBLIC_KEY = getattr(settings, "FLW_PRODUCTION_PUBLIC_KEY", "not set")
    FLW_SECRET_KEY = getattr(settings, "FLW_PRODUCTION_SECRET_KEY", "not set")
