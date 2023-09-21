from django.shortcuts import render
from .models import User
from .api.serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate

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
                'message': 'A senha deve conter no mínimo 8 caracteres!'
            }, status=status.HTTP_409_CONFLICT)
        password = request.data['password'].encode('utf-8')
        request.data['password'] = md5(password).hexdigest()
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
        

class LoginView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        password = request.data['password'].encode('utf-8')
        hashPassword = md5(password).hexdigest()
        user = authenticate(email=request.data['email'], password=hashPassword)
        if user is not None:
            return Response({
                'user': user,
                'token': user.auth_token.key
            }, status=status.HTTP_200_OK)
        else:
            if(User.objects.filter(email=request.data['email']).exists() == False):
                return Response({
                    'error': True,
                    'message': 'Este e-mail não está cadastrado!'
                }, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({
                    'error': True,
                    'message': 'Senha incorreta!'
                }, status=status.HTTP_401_UNAUTHORIZED)