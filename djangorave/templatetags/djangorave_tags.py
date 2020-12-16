# stdlib imports
import json

# django imports
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.utils import timezone
from django import template

# 3rd party imports

# project imports
from djangorave.models import DRPaymentTypeModel
from djangorave import settings
from djangorave.utils import create_integrity_hash


register = template.Library()
UserModel = get_user_model()


@register.simple_tag()
def pay_button_params(user_pk: str, payment_type_pk: str) -> str:
    """Returns params required when submitting a payment request to rave.

    Returns:
        txref: created by combining payment_type_pk, timestamp and user_pk
        redirect_url: transaction detail page to redirect to
        pub_key: PBFPubKey from settings
        integrity_hash: used by rave to ensure client side values are not altered
    """
    now = timezone.now().timestamp()
    txref = f"{payment_type_pk}__{now}__{user_pk}"
    redirect_url = reverse("djangorave:reference", kwargs={"reference": txref})
    payment_type = DRPaymentTypeModel.objects.get(pk=payment_type_pk)
    user = UserModel.objects.get(pk=user_pk)
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
