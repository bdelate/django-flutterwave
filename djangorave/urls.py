# stdlib  imports

# django imports
from django.urls import path, include

# 3rd party imports

# project imports
from djangorave.views import TransactionCreateView, TransactionDetailView


app_name = "djangorave"

urlpatterns = [
    path("transaction/", TransactionCreateView.as_view(), name="transaction"),
    path("<str:reference>/", TransactionDetailView.as_view(), name="reference"),
]
