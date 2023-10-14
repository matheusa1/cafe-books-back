from django.shortcuts import render
from .models import User, Purchase
from .api.serializers import UserSerializer, PurchaseSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password

from django.views.decorators.csrf import csrf_exempt

from hashlib import md5

class UserAPIView(APIView):
    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        if(len(request.data['password']) < 6):
            return Response({
                'error': True,
                'message': 'A senha deve conter no mínimo 6 caracteres!'
            }, status=status.HTTP_409_CONFLICT)
        password = request.data['password']
        request.data['password'] = make_password(password)
        request.data['type'] = 'User'
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'error': False,
                'message': 'Usuário cadastrado com sucesso!'
            }, status=status.HTTP_201_CREATED)
        
        if serializer.errors:
            if(User.objects.filter(email=request.data['email']).exists()):
                return Response({
                    'error': True,
                    'message': 'Este e-mail já está cadastrado!'
                }, status=status.HTTP_409_CONFLICT)
            if (request.data['name'] == '' or request.data['email'] == '' or request.data['password'] == ''):
                return Response({
                    'error': True,
                    'message': 'Todos os campos são obrigatórios!'
                }, status=status.HTTP_409_CONFLICT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class PurchaseAPIView(APIView):
    def get(self, request):
        purchase = Purchase.objects.all()
        serializer = PurchaseSerializer(purchase, many=True)
        return Response(serializer.data)
    