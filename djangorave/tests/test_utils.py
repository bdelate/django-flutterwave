# python import
from unittest.mock import patch

# django imports
from django.test import TestCase, override_settings

# 3rd party imports

# project imports
from djangorave.tests.factories import (
    PlanModelFactory,
    OnceOffModelFactory,
    UserFactory,
)
from djangorave.utils import create_integrity_hash


# @override_settings(RAVE_SANDBOX=True, RAVE_SANDBOX_PUBLIC_KEY="tesdfst")
class TestUtils(TestCase):
    """Test suite for djangorave utils"""

    @patch("djangorave.utils.settings")
    def test_create_plan_integrity_hash(self, mock_rave_settings):
        """Ensure the correct hash is returned for a plan"""
        mock_rave_settings.PUBLIC_KEY = "test"
        mock_rave_settings.SECRET_KEY = "test"
        pay_model = PlanModelFactory(
            amount=10,
            currency="USD",
            custom_logo="http://example.com/eg.png",
            custom_title="test",
            pay_button_text="test",
            payment_options="card",
            payment_plan=1,
        )
        user = UserFactory(first_name="test", last_name="test", email="test")
        txref = "12345"

        expected_hash = (
            "fb77a1ce99ecab8aba012dc79ac335cd7d97886d4e10620a5a78a5d100fe047b"
        )
        actual_hash = create_integrity_hash(pay_model=pay_model, user=user, txref=txref)
        self.assertEqual(expected_hash, actual_hash)

    @patch("djangorave.utils.settings")
    def test_create_onceoff_integrity_hash(self, mock_rave_settings):
        """Ensure the correct hash is returned for a plan"""
        mock_rave_settings.PUBLIC_KEY = "test"
        mock_rave_settings.SECRET_KEY = "test"
        pay_model = OnceOffModelFactory(
            amount=10,
            currency="USD",
            custom_logo="http://example.com/eg.png",
            custom_title="test",
            pay_button_text="test",
            payment_options="card",
        )
        user = UserFactory(first_name="test", last_name="test", email="test")
        txref = "12345"

        expected_hash = (
            "d2df044a25e0efcd9f42088328994420bcbfcd6ada43b5ae424af0fcdc6962d3"
        )
        actual_hash = create_integrity_hash(pay_model=pay_model, user=user, txref=txref)
        self.assertEqual(expected_hash, actual_hash)
