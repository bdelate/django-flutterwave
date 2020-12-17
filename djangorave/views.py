# stdlib imports

# django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView

# 3rd party imports
from rest_framework.generics import CreateAPIView

# project imports
from djangorave.models import DRTransactionModel, DRPaymentTypeModel
from djangorave.serializers import DRTransactionSerializer


UserModel = get_user_model()


class TransactionDetailView(LoginRequiredMixin, TemplateView):
    """Returns a transaction template"""

    template_name = "djangorave/transaction.html"

    def get_context_data(self, **kwargs):
        """Add transaction to context data"""
        kwargs = super().get_context_data(**kwargs)
        try:
            kwargs["transaction"] = DRTransactionModel.objects.get(
                user=self.request.user, reference=self.kwargs["reference"]
            )
        except DRTransactionModel.DoesNotExist:
            kwargs["transaction"] = None
        return kwargs


class TransactionCreateView(CreateAPIView):
    """Provides an api end point to create transactions"""

    queryset = DRTransactionModel.objects.all()
    serializer_class = DRTransactionSerializer
    authentication_classes: list = []

    def perform_create(self, serializer: DRTransactionSerializer) -> None:
        """Add payment_type and user to Transaction instance, determined
        from the received reference"""
        reference = serializer.validated_data["reference"]
        payment_type_id = reference.split("__")[0]
        user_id = reference.split("__")[2]
        serializer.save(
            user=UserModel.objects.get(id=user_id),
            payment_type=DRPaymentTypeModel.objects.get(id=payment_type_id),
        )
