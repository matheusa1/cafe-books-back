from rest_framework import serializers
from user import models

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'

class PurchaseItemSerializer(serializers.ModelSerializer):
    book_isbn = serializers.CharField(source='book.isbn')    
    class Meta:
        model = models.PurchaseItem
        fields = ['book_isbn', 'quantity', 'price']

class PurchaseSerializer(serializers.ModelSerializer): 
    books = PurchaseItemSerializer(source='purchaseitem_set', many=True, read_only=True)
    
    class Meta:
        model = models.Purchase
        fields = ['id', 'user', 'date', 'total', 'books', 'address', 'status']
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(CustomTokenObtainPairSerializer, cls).get_token(user)

        token['type'] = user.type
        token['username'] = user.username
        token['address'] = user.address
        token['phone'] = user.phone
        token['sex'] = user.sex               

        return token