# stdlib imports

# django imports

# 3rd party imports
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet

# project imports
from djangorave.models import TransactionModel
from djangorave.serializers import TransactionSerializer


class TransactionApiView(CreateModelMixin, GenericViewSet):
    """Provides ability create transactions"""

    queryset = TransactionModel.objects.all()
    serializer_class = TransactionSerializer
    # permission_classes = (ConfigListRetrieveUpdatePermission,)

    def perform_create(self, serializer):
        print("here" * 10)
        serializer.save(user=self.request.user)
