# stdlib imports
from typing import Union
import hashlib

# django imports
from django.contrib.auth.models import User

# 3rd party imports

# project imports
from djangorave.models import PlanModel, OnceOffModel
from djangorave.settings import PUBLIC_KEY, SECRET_KEY


def create_integrity_hash(
    pay_model: Union[PlanModel, OnceOffModel], user: User, txref: str
) -> str:
    """Returns an integrity hash created from the provided user and payment 
    details which is used by rave to ensure client side values are not altered."""
    data = {
        "PBFPubKey": PUBLIC_KEY,
        "amount": pay_model.amount,
        "currency": pay_model.currency,
        "custom_logo": pay_model.custom_logo,
        "custom_title": pay_model.custom_title,
        "customer_email": user.email,
        "customer_firstname": user.first_name,
        "customer_lastname": user.last_name,
        "pay_button_text": pay_model.pay_button_text,
        "payment_options": pay_model.payment_options,
        "payment_plan": getattr(pay_model, "payment_plan", ""),
        "txref": txref,
    }
    hash_string = ""
    for key in sorted(data.keys()):
        hash_string += str(data[key])
    hash_string += SECRET_KEY
    return hashlib.sha256(hash_string.encode("utf-8")).hexdigest()
