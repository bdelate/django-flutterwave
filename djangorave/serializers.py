# stdlib imports

# django imports
from django.contrib.auth import get_user_model

# 3rd party imports
from rest_framework import serializers

# project imports
from djangorave.models import DRTransactionModel, DRPaymentTypeModel


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for the Transaction Model"""

    txRef = serializers.CharField(source="reference")
    flwRef = serializers.CharField(source="flutterwave_reference")
    orderRef = serializers.CharField(source="order_reference")

    class Meta:
        model = DRTransactionModel
        fields = ("txRef", "flwRef", "orderRef", "amount", "charged_amount", "status")

    def validate_reference(self, value: str) -> str:
        """Ensure the received reference contains a valid payment_type_id and
        user_id"""
        payment_type_id = value.split("__")[0]
        user_id = value.split("__")[2]

        try:
            DRPaymentTypeModel.objects.get(id=payment_type_id)
        except DRPaymentTypeModel.DoesNotExist:
            raise serializers.ValidationError("Payment type does not exist")

        UserModel = get_user_model()
        payment_type_id = value.split("__")[0]
        try:
            UserModel.objects.get(id=user_id)
        except UserModel.DoesNotExist:
            raise serializers.ValidationError("User does not exist")

        return value
