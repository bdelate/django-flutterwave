# stdlib imports

# django imports
from django.contrib.auth import get_user_model

# 3rd party imports
from factory import fuzzy, DjangoModelFactory
import factory

# project imports
from djangorave.models import PaymentTypeModel, TransactionModel


class PaymentTypeModelFactory(DjangoModelFactory):
    """Factory for the PaymentTypeModel"""

    description = factory.Faker("word")
    amount = fuzzy.FuzzyDecimal(low=20, high=100, precision=2)
    currency = fuzzy.FuzzyChoice(choices=["USD", "ZAR", "EUR"])
    custom_title = factory.Faker("word")

    class Meta:
        model = PaymentTypeModel


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


class TransactionModelFactory(DjangoModelFactory):
    """Factory for the TransactionModel"""

    payment_type = factory.SubFactory(PaymentTypeModelFactory)
    user = factory.SubFactory(UserFactory)
    reference = factory.Faker("word")
    flutterwave_reference = factory.Faker("word")
    order_reference = factory.Faker("word")
    amount = fuzzy.FuzzyDecimal(low=20, high=100, precision=2)
    charged_amount = fuzzy.FuzzyDecimal(low=20, high=100, precision=2)
    status = fuzzy.FuzzyChoice(choices=["successful", "failed"])

    class Meta:
        model = TransactionModel
