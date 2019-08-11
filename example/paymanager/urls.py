# stdlib imports

# django imports
from django.urls import path, include

# 3rd party imports

# project imports
from paymanager.views import SignUpView

app_name = "paymanager"

urlpatterns = [path("", SignUpView.as_view(), name="signup")]
