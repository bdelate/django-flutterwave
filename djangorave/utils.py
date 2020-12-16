# stdlib imports
import hashlib

# django imports
from django.contrib.auth.models import User

# 3rd party imports

# project imports
from djangorave.models import DRPaymentTypeModel
from djangorave import settings


def create_integrity_hash(
    payment_type: DRPaymentTypeModel, user: User, txref: str, redirect_url: str
) -> str:
    """Returns an integrity hash created from the provided user and payment 
    details which is used by rave to ensure client side values are not altered."""
    data = {
        "PBFPubKey": settings.PUBLIC_KEY,
        "amount": payment_type.amount,
        "currency": payment_type.currency,
        "custom_logo": payment_type.custom_logo,
        "custom_title": payment_type.custom_title,
        "customer_email": user.email,
        "customer_firstname": user.first_name,
        "customer_lastname": user.last_name,
        "pay_button_text": payment_type.pay_button_text,
        "payment_options": payment_type.payment_options,
        "payment_plan": payment_type.payment_plan,
        "redirect_url": redirect_url,
        "txref": txref,
    }
    hash_string = ""
    for key in sorted(data.keys()):
        hash_string += str(data[key])
    hash_string += settings.SECRET_KEY
    return hashlib.sha256(hash_string.encode("utf-8")).hexdigest()
