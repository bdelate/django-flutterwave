# stdlib imports

# django imports
from django.contrib.auth import get_user_model

# 3rd party imports
from rest_framework import serializers

# project imports
from djangorave.models import DRTransactionModel, DRPaymentTypeModel


UserModel = get_user_model()


class DRTransactionSerializer(serializers.ModelSerializer):
    """Serializer for the DRTransactionModel Model"""

    txRef = serializers.CharField(source="reference")
    flwRef = serializers.CharField(source="flutterwave_reference")
    orderRef = serializers.CharField(source="order_reference")

    class Meta:
        model = DRTransactionModel
        fields = ("txRef", "flwRef", "orderRef", "amount", "charged_amount", "status")

    def validate_reference(self, value: str) -> str:
        """Ensure the received reference contains a valid payment_type_id and
        user_id"""
        try:
            payment_type_id = value.split("__")[0]
            DRPaymentTypeModel.objects.get(id=payment_type_id)
        except DRPaymentTypeModel.DoesNotExist:
            raise serializers.ValidationError("Payment type does not exist")

        try:
            user_id = value.split("__")[2]
            UserModel.objects.get(id=user_id)
        except UserModel.DoesNotExist:
            raise serializers.ValidationError("User does not exist")

        return value
