# stdlib imports

# django imports
from django.shortcuts import reverse
from django.test import TestCase, RequestFactory

# 3rd party imports
from rest_framework.test import APITestCase, APIRequestFactory

# project imports
from djangorave.views import TransactionDetailView, TransactionCreateView
from djangorave.models import DRTransactionModel
from djangorave.serializers import TransactionSerializer
from djangorave.tests.factories import (
    DRPaymentTypeModelFactory,
    UserFactory,
    DRTransactionModelFactory,
)


class TestTransactionDetailView(TestCase):
    """Test suite for the TransactionDetailView"""

    def test_get_context_data(self):
        """Ensure a transaction is added to the context only if a valid
        user and reference is provided"""
        factory = RequestFactory()
        user = UserFactory()
        transaction = DRTransactionModelFactory(user=user)
        request = factory.get("test")
        request.user = user
        view = TransactionDetailView()
        view.request = request

        view.kwargs = {"reference": transaction.reference}
        context_data = view.get_context_data()
        self.assertEqual(transaction, context_data["transaction"])

        view.kwargs = {"reference": "invalid"}
        context_data = view.get_context_data()
        self.assertIsNone(context_data["transaction"])


class TestTransactionCreateView(APITestCase):
    """Test suite for the TransactionCreateView"""

    def test_perform_create(self):
        """Ensure the user and payment_type are gotten from the reference and
        saved to the Transaction instance"""
        user = UserFactory()
        payment_type = DRPaymentTypeModelFactory()
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
        view = TransactionCreateView()
        view.request = request
        serializer = TransactionSerializer(data=data)
        serializer.is_valid()
        view.perform_create(serializer=serializer)

        self.assertEqual(DRTransactionModel.objects.count(), 1)
        transaction = DRTransactionModel.objects.first()
        self.assertEqual(transaction.user.id, user.id)
        self.assertEqual(transaction.payment_type.id, payment_type.id)
