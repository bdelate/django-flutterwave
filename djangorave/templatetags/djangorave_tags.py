# stdlib imports
from typing import Union
import json

# django imports
from django.contrib.auth.models import User
from django.utils import timezone
from django import template

# 3rd party imports

# project imports
from djangorave.models import PlanModel, OnceOffModel
from djangorave.settings import PUBLIC_KEY, RAVE_INLINE_JS
from djangorave.utils import create_integrity_hash


register = template.Library()


@register.simple_tag()
def pay_button_params(user: User, pay_model: Union[PlanModel, OnceOffModel]) -> str:
    """Returns params required when submitting a payment request to rave.
    
    txref: created by combining pay_model.description, timestamp and user_id
    pub_key: PBFPubKey from settings
    integrity_hash: used by rave to ensure client side values are note altered
    """
    now = timezone.now().timestamp()
    txref = f"{pay_model.description}__{now}__user{user.id}"
    integrity_hash = create_integrity_hash(pay_model=pay_model, user=user, txref=txref)
    return json.dumps(
        {"txref": txref, "pub_key": PUBLIC_KEY, "integrity_hash": integrity_hash}
    )


@register.simple_tag()
def rave_inline_js() -> str:
    """Return the RAVE_INLINE_JS setting"""
    return RAVE_INLINE_JS
