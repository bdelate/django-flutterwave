# stdlib imports
from datetime import datetime
import pytz

# django imports
from django.contrib.auth import get_user_model

# 3rd party imports
from factory import fuzzy
from factory.django import DjangoModelFactory
import factory

# project imports
from djangoflutterwave.models import FlwPlanModel, FlwTransactionModel


class FlwPlanModelFactory(DjangoModelFactory):
    """Factory for the FlwPlanModel"""

    name = factory.Faker("word")
    amount = fuzzy.FuzzyDecimal(low=20, high=100, precision=2)
    currency = fuzzy.FuzzyChoice(choices=["USD", "ZAR", "EUR"])
    modal_title = factory.Faker("word")

    class Meta:
        model = FlwPlanModel


class UserFactory(DjangoModelFactory):
    """Factory for the User model"""

    username = factory.Faker("word")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "adminadmin")
    is_active = True
    is_staff = False
    is_superuser = False

    class Meta:
        model = get_user_model()


class FlwTransactionModelFactory(DjangoModelFactory):
    """Factory for the FlwTransactionModel"""

    plan = factory.SubFactory(FlwPlanModelFactory)
    user = factory.SubFactory(UserFactory)
    tx_ref = factory.Faker("word")
    flw_ref = factory.Faker("word")
    device_fingerprint = factory.Faker("word")
    amount = fuzzy.FuzzyDecimal(low=20, high=100, precision=2)
    currency = fuzzy.FuzzyChoice(choices=["USD", "ZAR", "EUR"])
    charged_amount = fuzzy.FuzzyDecimal(low=20, high=100, precision=2)
    app_fee = fuzzy.FuzzyDecimal(low=1, high=5, precision=2)
    merchant_fee = fuzzy.FuzzyDecimal(low=1, high=5, precision=2)
    processor_response = factory.Faker("word")
    auth_model = factory.Faker("word")
    ip = factory.Faker("word")
    narration = factory.Faker("word")
    status = fuzzy.FuzzyChoice(choices=["successful", "failed"])
    payment_type = fuzzy.FuzzyChoice(choices=["card", "ussd"])
    created_at = fuzzy.FuzzyDateTime(
        start_dt=datetime(2018, 8, 15, tzinfo=pytz.UTC),
        end_dt=datetime(2020, 8, 15, tzinfo=pytz.UTC),
    )
    account_id = fuzzy.FuzzyInteger(low=1, high=100)

    class Meta:
        model = FlwTransactionModel
