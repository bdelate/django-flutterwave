# stdlib  imports

# django imports
from django.urls import path, include

# 3rd party imports
from rest_framework.routers import DefaultRouter

# project imports
from djangorave.views import TransactionCreateView, TransactionDetailView


app_name = "djangorave"

router = DefaultRouter()

router.register("transaction", TransactionCreateView, basename="transaction")

urlpatterns = [
    path("", include(router.urls)),
    path("<str:reference>/", TransactionDetailView.as_view(), name="reference"),
]
