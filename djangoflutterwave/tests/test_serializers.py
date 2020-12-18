# stdlib imports

# django imports
from django.test import TestCase

# 3rd party imports
from rest_framework.exceptions import ValidationError

# project imports
from djangoflutterwave.serializers import DRTransactionSerializer
from djangoflutterwave.tests.factories import FlwPlanModelFactory, UserFactory


class TestDRTransactionSerializer(TestCase):
    """Test suite for the DRTransactionSerializer"""

    def test_validate_reference(self):
        """Ensure the serializer raises an exception for an invalid
        plan_id or user_id """
        plan = FlwPlanModelFactory()
        user = UserFactory()

        expected_response = f"{plan.id}__test__{user.id}"
        actual_response = DRTransactionSerializer.validate_reference(
            self=None, value=expected_response
        )
        self.assertEqual(expected_response, actual_response)

        with self.assertRaises(ValidationError) as e:
            DRTransactionSerializer.validate_reference(
                self=None, value=f"123__test__{user.id}"
            )
        self.assertEqual(e.exception.detail[0], "Payment type does not exist")

        with self.assertRaises(ValidationError) as e:
            DRTransactionSerializer.validate_reference(
                self=None, value=f"{plan.id}__test__123"
            )
        self.assertEqual(e.exception.detail[0], "User does not exist")
