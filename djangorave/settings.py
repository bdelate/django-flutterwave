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
    RAVE_INLINE_JS = getattr(
        settings,
        "RAVE_SANDBOX_INLINE_JS",
        "https://ravesandboxapi.flutterwave.com/flwv3-pug/getpaidx/api/flwpbf-inline.js",
    )
else:
    PUBLIC_KEY = getattr(settings, "RAVE_PRODUCTION_PUBLIC_KEY", "not set")
    SECRET_KEY = getattr(settings, "RAVE_PRODUCTION_SECRET_KEY", "not set")
    RAVE_INLINE_JS = getattr(
        settings,
        "RAVE_PRODUCTION_INLINE_JS",
        "https://api.ravepay.co/flwv3-pug/getpaidx/api/flwpbf-inline.js",
    )
