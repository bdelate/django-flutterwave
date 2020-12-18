# stdlib imports
import json

# django imports
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.utils import timezone
from django import template

# 3rd party imports

# project imports
from djangorave.models import DRPlanModel
from djangorave import settings


register = template.Library()
UserModel = get_user_model()


@register.simple_tag()
def pay_button_params(user_pk: str, plan_pk: str) -> str:
    """Returns params required when submitting a payment request to rave.

    Returns:
        tx_ref: created by combining plan_pk, timestamp and user_pk
        redirect_url: transaction detail page to redirect to
        public_key: public key from settings
    """
    now = timezone.now().timestamp()
    tx_ref = f"{plan_pk}__{now}__{user_pk}"
    redirect_url = reverse("djangorave:transaction_detail", kwargs={"tx_ref": tx_ref})
    plan = DRPlanModel.objects.get(pk=plan_pk)
    user = UserModel.objects.get(pk=user_pk)
    return json.dumps(
        {
            "tx_ref": tx_ref,
            "redirect_url": redirect_url,
            "public_key": settings.FLW_PUBLIC_KEY,
        }
    )
