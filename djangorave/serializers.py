# stdlib imports

# django imports

# 3rd party imports
from rest_framework import serializers

# project imports
from djangorave.models import TransactionModel


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for the Transaction Model"""

    class Meta:
        model = TransactionModel
        fields = "__all__"
