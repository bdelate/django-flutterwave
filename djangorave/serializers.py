# stdlib imports

# django imports
from django.contrib.auth import get_user_model

# 3rd party imports
from rest_framework import serializers

# project imports
from djangorave.models import TransactionModel, PaymentMethodModel


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for the Transaction Model"""

    class Meta:
        model = TransactionModel
        fields = (
            "reference",
            "flutterwave_reference",
            "order_reference",
            "amount",
            "charged_amount",
            "status",
        )

    def validate_reference(self, value: str) -> str:
        """Ensure the received reference contains a valid payment_method_id and
        user_id"""
        payment_method_id = value.split("__")[0]
        user_id = value.split("__")[2]

        try:
            PaymentMethodModel.objects.get(id=payment_method_id)
        except PaymentMethodModel.DoesNotExist:
            raise serializers.ValidationError("Payment method does not exist")

        UserModel = get_user_model()
        payment_method_id = value.split("__")[0]
        try:
            UserModel.objects.get(id=user_id)
        except UserModel.DoesNotExist:
            raise serializers.ValidationError("User does not exist")

        return value
