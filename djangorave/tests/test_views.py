# stdlib imports

# django imports
from django.shortcuts import reverse
from django.test import TestCase, RequestFactory

# 3rd party imports
from rest_framework.test import APITestCase, APIRequestFactory

# project imports
from djangorave.views import TransactionDetailView, TransactionCreateView
from djangorave.models import DRTransactionModel
from djangorave.serializers import DRTransactionSerializer
from djangorave.tests.factories import (
    DRPlanModelFactory,
    UserFactory,
    DRTransactionModelFactory,
)


class TestTransactionDetailView(TestCase):
    """Test suite for the TransactionDetailView"""

    def test_get_context_data(self):
        """Ensure a transaction is added to the context only if a valid user and
        reference is provided"""
        factory = RequestFactory()
        user = UserFactory()
        transaction = DRTransactionModelFactory(user=user)
        request = factory.get("test")
        request.user = user
        view = TransactionDetailView()
        view.request = request

        view.kwargs = {"tx_ref": transaction.tx_ref}
        context_data = view.get_context_data()
        self.assertEqual(transaction, context_data["transaction"])

        view.kwargs = {"tx_ref": "invalid"}
        context_data = view.get_context_data()
        self.assertIsNone(context_data["transaction"])


class TestTransactionCreateView(APITestCase):
    """Test suite for the TransactionCreateView"""

    def test_perform_create(self):
        """Ensure the user and plan are gotten from the reference and saved to the
        Transaction instance"""
        user = UserFactory()
        plan = DRPlanModelFactory()
        factory = APIRequestFactory()
        data = {
            "tx_ref": f"{plan.id}__test__{user.id}",
            "flw_ref": "test",
            "device_fingerprint": "test",
            "amount": 10.00,
            "currency": "USD",
            "charged_amount": 9.00,
            "app_fee": 0.50,
            "merchant_fee": 0.50,
            "processor_response": "test",
            "auth_model": "test",
            "ip": "test",
            "narration": "test",
            "status": "test",
            "payment_type": "test",
            "created_at": "test",
            "account_id": 123,
        }
        request = factory.post("fake-url", data)
        request.user = user
        view = TransactionCreateView()
        view.request = request
        serializer = DRTransactionSerializer(data=data)
        serializer.is_valid()
        view.perform_create(serializer=serializer)

        self.assertEqual(DRTransactionModel.objects.count(), 1)
        transaction = DRTransactionModel.objects.first()
        self.assertEqual(transaction.user.id, user.id)
        self.assertEqual(transaction.plan.id, plan.id)
