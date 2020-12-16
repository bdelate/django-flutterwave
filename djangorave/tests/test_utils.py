# python import
from unittest.mock import patch

# django imports
from django.test import TestCase

# 3rd party imports

# project imports
from djangorave.tests.factories import DRPaymentTypeModelFactory, UserFactory
from djangorave.utils import create_integrity_hash


class TestUtils(TestCase):
    """Test suite for djangorave utils"""

    @patch("djangorave.utils.settings")
    def test_create_plan_integrity_hash(self, mock_rave_settings):
        """Ensure the correct hash is returned for a plan"""
        mock_rave_settings.PUBLIC_KEY = "test"
        mock_rave_settings.SECRET_KEY = "test"
        payment_type = DRPaymentTypeModelFactory(
            amount=10,
            currency="USD",
            custom_logo="http://example.com/eg.png",
            custom_title="test",
            pay_button_text="test",
            payment_options="card",
            payment_plan=1,
        )
        user = UserFactory(first_name="test", last_name="test", email="test@test.com")
        txref = "12345"
        redirect_url = "test"

        expected_response = (
            "1e2b7754ee03721e2bca37680cc5cb973b41addf446a8b791a8bc97e6eaa652c"
        )
        actual_response = create_integrity_hash(
            payment_type=payment_type, user=user, txref=txref, redirect_url=redirect_url
        )
        self.assertEqual(expected_response, actual_response)

    @patch("djangorave.utils.settings")
    def test_create_onceoff_integrity_hash(self, mock_rave_settings):
        """Ensure the correct hash is returned for a onceoff payment"""
        mock_rave_settings.PUBLIC_KEY = "test"
        mock_rave_settings.SECRET_KEY = "test"
        payment_type = DRPaymentTypeModelFactory(
            amount=10,
            currency="USD",
            custom_logo="http://example.com/eg.png",
            custom_title="test",
            pay_button_text="test",
            payment_options="card",
        )
        user = UserFactory(first_name="test", last_name="test", email="test@test.com")
        txref = "12345"
        redirect_url = "test"

        expected_response = (
            "8d5aa47bc2b280aeb0815ef7ace05c87bd25d69276cbc12ac82c5cfe7a9d5d52"
        )
        actual_response = create_integrity_hash(
            payment_type=payment_type, user=user, txref=txref, redirect_url=redirect_url
        )
        self.assertEqual(expected_response, actual_response)
