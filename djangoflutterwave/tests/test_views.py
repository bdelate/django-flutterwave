# stdlib imports
from datetime import datetime
from unittest.mock import patch

# django imports
from django.test import TestCase, RequestFactory

# 3rd party imports
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIRequestFactory

# project imports
from djangoflutterwave.views import (
    TransactionDetailView,
    TransactionCreateView,
    PaymentParamsView,
)
from djangoflutterwave.models import FlwTransactionModel
from djangoflutterwave.serializers import DRTransactionSerializer
from djangoflutterwave.tests.factories import (
    FlwPlanModelFactory,
    UserFactory,
    FlwTransactionModelFactory,
)


class TestTransactionDetailView(TestCase):
    """Test suite for the TransactionDetailView"""

    def test_get_context_data(self):
        """Ensure a transaction is added to the context only if a valid user and
        reference is provided"""
        factory = RequestFactory()
        user = UserFactory()
        transaction = FlwTransactionModelFactory(user=user)
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
        plan = FlwPlanModelFactory()
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
            "created_at": datetime.now(),
            "account_id": 123,
        }
        request = factory.post("fake-url", data)
        request.user = user
        view = TransactionCreateView()
        view.request = request
        serializer = DRTransactionSerializer(data=data)
        serializer.is_valid()
        view.perform_create(serializer=serializer)

        self.assertEqual(FlwTransactionModel.objects.count(), 1)
        transaction = FlwTransactionModel.objects.first()
        self.assertEqual(transaction.user.id, user.id)
        self.assertEqual(transaction.plan.id, plan.id)


class TestPaymentParamsView(APITestCase):
    """Test suite for the PaymentParamsView"""

    @patch("djangoflutterwave.views.settings")
    @patch("djangoflutterwave.views.create_transaction_ref")
    def test_get(self, mock_create_transaction_ref, mock_settings):
        """Ensure valid data is returned if a valid plan is provided"""
        mock_create_transaction_ref.return_value = "ref"
        mock_settings.FLW_PUBLIC_KEY = "pub_key"
        user = UserFactory()
        plan = FlwPlanModelFactory()
        factory = APIRequestFactory()
        view = PaymentParamsView()

        url = reverse("djangoflutterwave:payment_params")
        request = factory.get(url)
        request.user = user
        view.request = request
        res = view.get(request=request)
        self.assertEqual(res.data, "Plan does not exist")

        expected_res = {
            "public_key": "pub_key",
            "tx_ref": "ref",
            "amount": plan.amount,
            "currency": plan.currency,
            "payment_plan": plan.flw_plan_id,
            "customer": {
                "email": user.email,
                "name": f"{user.first_name} {user.last_name}",
            },
            "customizations": {"title": plan.modal_title, "logo": plan.modal_logo_url},
        }
        request = factory.get(f"{url}?plan={plan.name}")
        request.user = user
        view.request = request
        res = view.get(request=request)
        self.assertEqual(res.data, expected_res)
