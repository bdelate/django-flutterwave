# stdlib imports

# django imports
from django.contrib.auth import get_user_model

# 3rd party imports
from factory import fuzzy, DjangoModelFactory
import factory

# project imports
from djangorave.models import PlanModel, OnceOffModel


class PaymentBaseModelFactory(DjangoModelFactory):
    """Factory for the PaymentBaseModel"""

    description = factory.Faker("word")
    amount = fuzzy.FuzzyDecimal(low=20, high=100, precision=2)
    currency = fuzzy.FuzzyChoice(choices=["USD", "ZAR", "EUR"])
    custom_title = factory.Faker("word")


class PlanModelFactory(PaymentBaseModelFactory):
    """Factory for the PlanModel"""

    payment_plan = fuzzy.FuzzyInteger(low=1, high=100)

    class Meta:
        model = PlanModel


class OnceOffModelFactory(PaymentBaseModelFactory):
    """Factory for the OnceOffModel"""

    class Meta:
        model = OnceOffModel


class UserFactory(DjangoModelFactory):
    """Factory for the User model"""

    username = factory.Faker("word")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "secret")
    is_active = True
    is_staff = False
    is_superuser = False

    class Meta:
        model = get_user_model()
