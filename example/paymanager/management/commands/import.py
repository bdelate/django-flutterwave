# stdlib imports
import sys

# django imports
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

# 3rd party imports

# project imports
from djangorave.models import PaymentTypeModel
from djangorave.tests.factories import PaymentTypeModelFactory, UserFactory


class Command(BaseCommand):
    """Management command for import dev environment data"""

    help = "Creates payment types to enable a working example"

    def handle(self, *args, **kwargs):
        get_user_model().objects.all().delete()
        UserFactory(username="testuser", is_staff=True, is_superuser=True)

        PaymentTypeModel.objects.all().delete()
        PaymentTypeModelFactory(
            description="Once off Purchase",
            custom_title="Purchase this item",
            currency="USD",
            pay_button_text="Buy Now",
        )
        PaymentTypeModelFactory(
            description="Subscription Plan",
            custom_title="Sign Up to this plan",
            currency="USD",
            pay_button_text="Sign Up",
            payment_plan=123,
        )
        print("\nData imported")
