# stdlib imports
import sys

# django imports
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

# 3rd party imports

# project imports
from djangorave.models import DRPlanModel
from djangorave.tests.factories import DRPlanModelFactory, UserFactory


class Command(BaseCommand):
    """Management command for import dev environment data"""

    help = "Creates payment types to enable a working example"

    def handle(self, *args, **kwargs):
        get_user_model().objects.all().delete()
        UserFactory(username="admin", is_staff=True, is_superuser=True)

        DRPlanModel.objects.all().delete()
        DRPlanModelFactory(
            name="Once off Purchase",
            modal_title="Purchase this item",
            currency="USD",
            pay_button_text="Buy Now",
        )
        DRPlanModelFactory(
            name="Subscription Plan",
            modal_title="Sign Up to this plan",
            currency="USD",
            pay_button_text="Sign Up",
            flw_plan_id=123,
        )
        print("\nData imported")
