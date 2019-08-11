# stdlib imports

# django imports
from django.views.generic import TemplateView

# 3rd party imports

# project imports
from djangorave.models import TransactionModel


class TransactionView(TemplateView):
    """Returns a transaction template"""

    template_name = "djangorave/transaction.html"

    def get_context_data(self, **kwargs):
        """Add plan to context data"""
        context_data = super().get_context_data(**kwargs)
        try:
            context_data["transaction"] = TransactionModel.objects.get(
                reference=self.kwargs["reference"]
            )
        except TransactionModel.DoesNotExist:
            context_data["transaction"] = None
        return context_data
