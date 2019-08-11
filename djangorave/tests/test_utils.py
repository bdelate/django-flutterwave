# python import
from unittest.mock import patch

# django imports
from django.test import TestCase

# 3rd party imports

# project imports
from djangorave.tests.factories import PaymentMethodModelFactory, UserFactory
from djangorave.utils import create_integrity_hash


class TestUtils(TestCase):
    """Test suite for djangorave utils"""

    @patch("djangorave.utils.settings")
    def test_create_plan_integrity_hash(self, mock_rave_settings):
        """Ensure the correct hash is returned for a plan"""
        mock_rave_settings.PUBLIC_KEY = "test"
        mock_rave_settings.SECRET_KEY = "test"
        payment_method = PaymentMethodModelFactory(
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

        expected_response = (
            "feb3402878b204ce830de3d4b812721f1d017ec71a9855247bb4d16ab263c77e"
        )
        actual_response = create_integrity_hash(
            payment_method=payment_method, user=user, txref=txref
        )
        self.assertEqual(expected_response, actual_response)

    @patch("djangorave.utils.settings")
    def test_create_onceoff_integrity_hash(self, mock_rave_settings):
        """Ensure the correct hash is returned for a onceoff payment"""
        mock_rave_settings.PUBLIC_KEY = "test"
        mock_rave_settings.SECRET_KEY = "test"
        payment_method = PaymentMethodModelFactory(
            amount=10,
            currency="USD",
            custom_logo="http://example.com/eg.png",
            custom_title="test",
            pay_button_text="test",
            payment_options="card",
        )
        user = UserFactory(first_name="test", last_name="test", email="test@test.com")
        txref = "12345"

        expected_response = (
            "3e76fa15d1651c2e69073aa0ec9af1679ddc5b7c20253fece1bb9f03f1a7df91"
        )
        actual_response = create_integrity_hash(
            payment_method=payment_method, user=user, txref=txref
        )
        self.assertEqual(expected_response, actual_response)
