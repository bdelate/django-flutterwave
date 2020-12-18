# stdlib imports

# django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView

# 3rd party imports
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status

# project imports
from djangoflutterwave.models import FlwTransactionModel, FlwPlanModel
from djangoflutterwave.serializers import DRTransactionSerializer


UserModel = get_user_model()


class TransactionDetailView(LoginRequiredMixin, TemplateView):
    """Returns a transaction template"""

    template_name = "djangoflutterwave/transaction.html"

    def get_context_data(self, **kwargs):
        """Add transaction to context data"""
        kwargs = super().get_context_data(**kwargs)
        try:
            kwargs["transaction"] = FlwTransactionModel.objects.get(
                user=self.request.user, tx_ref=self.kwargs["tx_ref"]
            )
        except FlwTransactionModel.DoesNotExist:
            kwargs["transaction"] = None
        return kwargs


class TransactionCreateView(CreateAPIView):
    """Provides an api end point to create transactions"""

    queryset = FlwTransactionModel.objects.all()
    serializer_class = DRTransactionSerializer
    authentication_classes: list = []

    def create(self, request, *args, **kwargs):
        """Override create to specify request.data['data'] for serializer data"""
        serializer = self.get_serializer(data=request.data.get("data", None))
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer: DRTransactionSerializer) -> None:
        """Add plan and user to Transaction instance, determined from the received
        reference"""
        reference = serializer.validated_data["tx_ref"]
        plan_id = reference.split("__")[0]
        user_id = reference.split("__")[2]
        serializer.save(
            user=UserModel.objects.get(id=user_id),
            plan=FlwPlanModel.objects.get(id=plan_id),
        )
