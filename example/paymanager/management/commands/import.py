# stdlib imports
import sys

# django imports
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

# 3rd party imports

# project imports
from djangoflutterwave.models import FlwPlanModel
from djangoflutterwave.tests.factories import FlwPlanModelFactory, UserFactory


class Command(BaseCommand):
    """Management command for import dev environment data"""

    help = "Creates payment types to enable a working example"

    def handle(self, *args, **kwargs):
        get_user_model().objects.all().delete()
        UserFactory(username="admin", is_staff=True, is_superuser=True)

        FlwPlanModel.objects.all().delete()
        FlwPlanModelFactory(
            name="Once off Purchase",
            modal_title="Purchase this item",
            currency="USD",
            pay_button_text="Buy Now",
        )
        FlwPlanModelFactory(
            name="Subscription Plan",
            modal_title="Sign Up to this plan",
            currency="USD",
            pay_button_text="Sign Up",
            flw_plan_id=123,
        )
        print("\nData imported")
