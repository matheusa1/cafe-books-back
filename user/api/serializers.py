from rest_framework import serializers
from user import models

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'

class PurchaseSerializer(serializers.ModelSerializer): 
    class Meta:
        model = models.Purchase
        fields = '__all__'
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    @classmethod
    def get_token(cls, user):
        token = super(CustomTokenObtainPairSerializer, cls).get_token(user)

        token['type'] = user.type
        token['username'] = user.username
        token['address'] = user.address
        token['phone'] = user.phone
        token['sex'] = user.sex
        token['favorites'] = list(user.favorites.values_list('id', flat=True)) if user.favorites.exists() else []

        return token