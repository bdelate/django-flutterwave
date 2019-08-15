# stdlib imports

# django imports

# 3rd party imports
from rest_framework.test import APITestCase, APIRequestFactory

# project imports
from djangorave.views.api import TransactionApiView
from djangorave.models import TransactionModel
from djangorave.serializers import TransactionSerializer
from djangorave.tests.factories import PaymentTypeModelFactory, UserFactory


class TestTransactionApiView(APITestCase):
    """Test suite for the TransactionApiView"""

    def test_perform_create(self):
        """Ensure the user and payment_type are gotten from the reference and
        saved to the Transaction instance"""
        user = UserFactory()
        payment_type = PaymentTypeModelFactory()
        factory = APIRequestFactory()
        data = {
            "txRef": f"{payment_type.id}__test__{user.id}",
            "flwRef": "test",
            "orderRef": "test",
            "amount": 10,
            "charged_amount": 10,
            "status": "test",
        }
        request = factory.post("fake-url", data)
        request.user = user
        view = TransactionApiView()
        view.request = request
        serializer = TransactionSerializer(data=data)
        serializer.is_valid()
        view.perform_create(serializer=serializer)

        self.assertEqual(TransactionModel.objects.count(), 1)
        transaction = TransactionModel.objects.first()
        self.assertEqual(transaction.user.id, user.id)
        self.assertEqual(transaction.payment_type.id, payment_type.id)
