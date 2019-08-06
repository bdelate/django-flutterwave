# stdlib imports

# django imports
from django.urls import path

# 3rd party imports

# project imports
from paymanager.views import SignUpView
from djangorave.views import IndexView


app_name = "paymanager"

urlpatterns = [path("", SignUpView.as_view(), name="signup")]
# urlpatterns = [path("", IndexView.as_view(), name="index")]
