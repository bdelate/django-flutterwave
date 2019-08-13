# stdlib imports

# django imports
from django.contrib.auth import get_user_model

# 3rd party imports
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet

# project imports
from djangorave.models import TransactionModel, PaymentTypeModel
from djangorave.serializers import TransactionSerializer


class TransactionApiView(CreateModelMixin, GenericViewSet):
    """Provides an api end point to create transactions"""

    queryset = TransactionModel.objects.all()
    serializer_class = TransactionSerializer
    authentication_classes: list = []

    def perform_create(self, serializer: TransactionSerializer) -> None:
        """Add payment_type and user to Transaction instance, determined
        from the received reference"""
        reference = serializer.validated_data["reference"]
        payment_type_id = reference.split("__")[0]
        user_id = reference.split("__")[2]
        serializer.save(
            user=get_user_model().objects.get(id=user_id),
            payment_type=PaymentTypeModel.objects.get(id=payment_type_id),
        )
