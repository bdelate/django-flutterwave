# stdlib imports
from unittest.mock import patch

# django imports
from django.test import TestCase

# 3rd party imports

# project imports
from djangoflutterwave.tests.factories import FlwPlanModelFactory, UserFactory
from djangoflutterwave.utils import create_transaction_ref


class TestUtils(TestCase):
    """Test suite for utils"""

    @patch("djangoflutterwave.utils.timezone")
    def test_create_transaction_ref(self, mock_timezone):
        """Ensure the correct transaction ref is created"""
        mock_timezone.now.return_value.timestamp.return_value = "test"
        plan = FlwPlanModelFactory()
        user = UserFactory()
        res = create_transaction_ref(plan_pk=plan.pk, user_pk=user.pk)
        self.assertEqual(res, f"{plan.pk}__test__{user.pk}")
