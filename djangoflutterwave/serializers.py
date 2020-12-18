# stdlib imports

# django imports
from django.contrib.auth import get_user_model

# 3rd party imports
from rest_framework import serializers

# project imports
from djangoflutterwave.models import FlwTransactionModel, FlwPlanModel


UserModel = get_user_model()


class DRTransactionSerializer(serializers.ModelSerializer):
    """Serializer for the FlwTransactionModel Model"""

    class Meta:
        model = FlwTransactionModel
        fields = (
            "tx_ref",
            "flw_ref",
            "device_fingerprint",
            "amount",
            "currency",
            "charged_amount",
            "app_fee",
            "merchant_fee",
            "processor_response",
            "auth_model",
            "ip",
            "narration",
            "status",
            "payment_type",
            "created_at",
            "account_id",
        )

    def validate_reference(self, value: str) -> str:
        """Ensure the received reference contains a valid plan_id and
        user_id"""
        try:
            plan_id = value.split("__")[0]
            FlwPlanModel.objects.get(id=plan_id)
        except FlwPlanModel.DoesNotExist:
            raise serializers.ValidationError("Payment type does not exist")

        try:
            user_id = value.split("__")[2]
            UserModel.objects.get(id=user_id)
        except UserModel.DoesNotExist:
            raise serializers.ValidationError("User does not exist")

        return value
