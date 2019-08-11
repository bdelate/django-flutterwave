# stdlib imports
import json

# django imports
from django.contrib.auth.models import User
from django.utils import timezone
from django import template

# 3rd party imports

# project imports
from djangorave.models import PaymentMethodModel
from djangorave import settings
from djangorave.utils import create_integrity_hash


register = template.Library()


@register.simple_tag()
def pay_button_params(user: User, payment_method: PaymentMethodModel) -> str:
    """Returns params required when submitting a payment request to rave.

    txref: created by combining payment_method.id, timestamp and user_id
    pub_key: PBFPubKey from settings
    integrity_hash: used by rave to ensure client side values are note altered
    """
    now = timezone.now().timestamp()
    txref = f"{payment_method.id}__{now}__user_{user.id}"
    integrity_hash = create_integrity_hash(
        payment_method=payment_method, user=user, txref=txref
    )
    return json.dumps(
        {
            "txref": txref,
            "pub_key": settings.PUBLIC_KEY,
            "integrity_hash": integrity_hash,
        }
    )


@register.simple_tag()
def rave_inline_js() -> str:
    """Return the RAVE_INLINE_JS setting"""
    return settings.RAVE_INLINE_JS
