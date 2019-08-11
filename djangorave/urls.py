# stdlib  imports

# django imports
from django.urls import path, include

# 3rd party imports
from rest_framework.routers import DefaultRouter

# project imports
from djangorave.views.api import TransactionApiView
from djangorave.views.template import TransactionView


app_name = "djangorave"

router = DefaultRouter()

router.register("transaction", TransactionApiView, basename="transaction")

urlpatterns = [
    path("", include(router.urls)),
    path("<str:reference>/", TransactionView.as_view(), name="reference"),
]
