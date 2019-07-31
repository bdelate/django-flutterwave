# django imports
from django.urls import path

# project imports
from djangorave.views import IndexView


app_name = "djangorave"

urlpatterns = [path("", IndexView.as_view(), name="index")]
