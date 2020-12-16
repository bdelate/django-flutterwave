# stdlib imports
from unittest.mock import patch

# django imports
from django.test import TestCase

# 3rd party imports

# project imports
from djangorave.tests.factories import DRPaymentTypeModelFactory, UserFactory
from djangorave.templatetags.djangorave_tags import pay_button_params, rave_inline_js


class TestTemplateTags(TestCase):
    """Test suite for template tags"""

    @patch("djangorave.templatetags.djangorave_tags.create_integrity_hash")
    @patch("djangorave.templatetags.djangorave_tags.timezone")
    @patch("djangorave.templatetags.djangorave_tags.settings")
    @patch("djangorave.templatetags.djangorave_tags.reverse")
    def test_pay_button_params(
        self,
        mock_reverse,
        mock_rave_settings,
        mock_timezone,
        mock_create_integrity_hash,
    ):
        """Ensure a json string is returned containing the correct txref,
        pub_key and integrity_hash """
        mock_reverse.return_value = "test"
        mock_rave_settings.PUBLIC_KEY = "test"
        mock_timezone.now.return_value.timestamp.return_value = "test"
        mock_create_integrity_hash.return_value = "test"
        payment_type = DRPaymentTypeModelFactory()
        user = UserFactory()

        expected_response = (
            f'{{"txref": "{payment_type.id}__test__{user.id}"'
            ', "redirect_url": "test", "pub_key": "test", "integrity_hash": "test"}'
        )
        actual_response = pay_button_params(
            user_pk=user.pk, payment_type_pk=payment_type.pk
        )
        mock_create_integrity_hash.assert_called()
        mock_reverse.assert_called()
        self.assertEqual(expected_response, actual_response)

    @patch("djangorave.templatetags.djangorave_tags.settings")
    def test_rave_inline_js(self, mock_rave_settings):
        """Ensure the RAVE_INLINE_JS setting is returned"""
        mock_rave_settings.RAVE_INLINE_JS = "test"
        expected_response = "test"
        actual_response = rave_inline_js()
        self.assertEqual(expected_response, actual_response)
