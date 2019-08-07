# stdlib imports

# django imports

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
