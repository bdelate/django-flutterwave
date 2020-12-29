# stdlib imports
from unittest.mock import patch

# django imports
from django.test import TestCase

# 3rd party imports

# project imports
from djangoflutterwave.tests.factories import FlwPlanModelFactory, UserFactory
from djangoflutterwave.templatetags.djangoflutterwave_tags import pay_button_params


class TestTemplateTags(TestCase):
    """Test suite for template tags"""

    @patch(
        "djangoflutterwave.templatetags.djangoflutterwave_tags.create_transaction_ref"
    )
    @patch("djangoflutterwave.templatetags.djangoflutterwave_tags.settings")
    @patch("djangoflutterwave.templatetags.djangoflutterwave_tags.reverse")
    def test_pay_button_params(
        self, mock_reverse, mock_settings, mock_create_transaction_ref
    ):
        """Ensure a json string is returned containing the correct tx_ref,
        public_key and redirect_url"""
        mock_reverse.return_value = "test"
        mock_settings.FLW_PUBLIC_KEY = "test"
        mock_create_transaction_ref.return_value = "txref"
        plan = FlwPlanModelFactory()
        user = UserFactory()

        expected_response = (
            '{"tx_ref": "txref"' ', "redirect_url": "test", "public_key": "test"}'
        )
        actual_response = pay_button_params(user_pk=user.pk, plan_pk=plan.pk)
        mock_reverse.assert_called()
        self.assertEqual(expected_response, actual_response)
