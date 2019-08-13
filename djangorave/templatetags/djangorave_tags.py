# stdlib imports
import json

# django imports
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.utils import timezone
from django import template

# 3rd party imports

# project imports
from djangorave.models import PaymentTypeModel
from djangorave import settings
from djangorave.utils import create_integrity_hash


register = template.Library()


@register.simple_tag()
def pay_button_params(user: User, payment_type: PaymentTypeModel) -> str:
    """Returns params required when submitting a payment request to rave.

    Returns:
        txref: created by combining payment_type.id, timestamp and user_id
        redirect_url: transaction detail page to redirect to
        pub_key: PBFPubKey from settings
        integrity_hash: used by rave to ensure client side values are note altered
    """
    now = timezone.now().timestamp()
    txref = f"{payment_type.id}__{now}__{user.id}"
    redirect_url = reverse("djangorave:reference", kwargs={"reference": txref})
    integrity_hash = create_integrity_hash(
        payment_type=payment_type, user=user, txref=txref, redirect_url=redirect_url
    )
    return json.dumps(
        {
            "txref": txref,
            "redirect_url": redirect_url,
            "pub_key": settings.PUBLIC_KEY,
            "integrity_hash": integrity_hash,
        }
    )


@register.simple_tag()
def rave_inline_js() -> str:
    """Return the RAVE_INLINE_JS setting"""
    return settings.RAVE_INLINE_JS
