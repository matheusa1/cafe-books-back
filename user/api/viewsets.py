from rest_framework import viewsets
from user.api import serializers
from user import models

class UserViewsSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()

class PurchaseViewsSet(viewsets.ModelViewSet):
    serializer_class = serializers.PurchaseSerializer
    queryset = models.Purchase.objects.all()