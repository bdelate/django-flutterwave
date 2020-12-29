# stdlib imports
from typing import Union

# django imports
from django.utils import timezone

# 3rd party imports

# project imports


def create_transaction_ref(plan_pk: Union[str, int], user_pk: Union[str, int]):
    """Create transaction reference"""
    now = timezone.now().timestamp()
    return f"{plan_pk}__{now}__{user_pk}"
