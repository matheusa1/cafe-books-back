from django.shortcuts import render
from .models import User, Purchase, PurchaseItem, UserFavorites
from book.models import Book
from .api.serializers import UserSerializer, PurchaseSerializer
from book.api.serializers import BookSerializer
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
    
    def post(self, request):
        if(request.data['user'] == ''):
            return Response({
                'error': True,
                'message': 'Usuário não informado!'
            }, status=status.HTTP_409_CONFLICT)
        user = User.objects.get(id=request.data['user'])
        request.data['user'] = user.id
        if(request.data['books'] == []):
            return Response({
                'error': True,
                'message': 'Nenhum livro informado!'
            }, status=status.HTTP_409_CONFLICT)
        if(request.data['address'] == ''):
            if(user.address == ''):
                return Response({
                    'error': True,
                    'message': 'Endereço não informado!'
                }, status=status.HTTP_409_CONFLICT)
            else:
                request.data['address'] = user.address
        request.data['total'] = 0

        serializer = PurchaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            for book in request.data['books']:
                if(Book.objects.filter(isbn=book).exists() == False):
                    return Response({
                        'error': True,
                        'message': 'Este livro não existe!'
                    }, status=status.HTTP_409_CONFLICT)
                book = Book.objects.get(isbn=book)
                purchase = Purchase.objects.get(id=request.data['id'])
                purchase_item = PurchaseItem(purchase=purchase, book=book, price=book.price, quantity=1)
                purchase_item.save()
                purchase.total = purchase.total + book.price
                book.stock = book.stock - 1
                book.save()

            purchase.save()
            return Response({
                'error': False,
                'message': 'Compra cadastrada com sucesso!'
            }, status=status.HTTP_201_CREATED)

        if serializer.errors:
            if (request.data['user'] == '' or request.data['books'] == '' or request.data['address'] == ''):
                return Response({
                    'error': True,
                    'message': 'Todos os campos são obrigatórios!'
                }, status=status.HTTP_409_CONFLICT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request):
        purchase = Purchase.objects.get(id=request.data['id'])
        purchase.status = request.data['status']
        if request.data['books'] != []:
            for book in request.data['books']:
                if(Book.objects.filter(isbn=book).exists() == False):
                    return Response({
                        'error': True,
                        'message': 'Este livro não existe!'
                    }, status=status.HTTP_409_CONFLICT)
                book = Book.objects.get(isbn=book)
                purchase_item = PurchaseItem(purchase=purchase, book=book)
                purchase_item.save()
                purchase.total = purchase.total + book.price
                book.stock = book.stock - 1
                book.save()

        purchase.save()
        return Response({
            'error': False,
            'message': 'Status atualizado com sucesso!'
        }, status=status.HTTP_201_CREATED)
    def delete(self, request):
        purchase = Purchase.objects.get(id=request.data['id'])
        purchase.delete()
        return Response({
            'error': False,
            'message': 'Compra excluída com sucesso!'
        }, status=status.HTTP_201_CREATED)
    
class FavoritesAPIView(APIView):
    def get(self, request):
        user = User.objects.get(id=request.GET['user'])
        books = user.favorites.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        if(request.data['user'] == ''):
            return Response({
                'error': True,
                'message': 'Usuário não informado!'
            }, status=status.HTTP_409_CONFLICT)
        user = User.objects.get(id=request.data['user'])

        if(request.data['book'] == ''):
            return Response({
                'error': True,
                'message': 'Livro não informado!'
            }, status=status.HTTP_409_CONFLICT)
        if(Book.objects.filter(isbn=request.data['book']).exists() == False):
            return Response({
                'error': True,
                'message': 'Este livro não existe!'
            }, status=status.HTTP_409_CONFLICT)
        book = Book.objects.get(isbn=request.data['book'])

        if(user.favorites.filter(isbn=book.isbn).exists()):
            return Response({
                'error': True,
                'message': 'Este livro já está nos favoritos!'
            }, status=status.HTTP_409_CONFLICT)
        user_favorite = UserFavorites(user=user, book=book)
        user_favorite.save()
        return Response({
            'error': False,
            'message': 'Livro adicionado aos favoritos com sucesso!'
        }, status=status.HTTP_201_CREATED)
    
    def delete(self, request):
        user = User.objects.get(id=request.data['user'])
        book = Book.objects.get(isbn=request.data['book'])
        if(user.favorites.filter(isbn=book.isbn).exists() == False):
            return Response({
                'error': True,
                'message': 'Este livro não está nos favoritos!'
            }, status=status.HTTP_409_CONFLICT)
        user_favorite = UserFavorites.objects.get(user=user, book=book)
        user_favorite.delete()
        return Response({
            'error': False,
            'message': 'Livro removido dos favoritos com sucesso!'
        }, status=status.HTTP_201_CREATED)

class CartAPIView(APIView):
    def get(self, request):
        user = User.objects.get(id=request.GET['user'])
        if(user.cart == None):
            return Response({
                'error': True,
                'message': 'Carrinho vazio!'
            }, status=status.HTTP_409_CONFLICT)
        serializer = PurchaseSerializer(user.cart, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        user = User.objects.get(id=request.data['user'])
        if(user.cart == None):
            purchase = Purchase(user=user, status='Pendente')
            purchase.save()
            user.cart = purchase
            user.save()
        else:
            purchase = user.cart
            purchase.total = 0
        
        if(request.data['book'] == ''):
            return Response({
                'error': True,
                'message': 'Nenhum livro informado!'
            }, status=status.HTTP_409_CONFLICT)
        
        book = Book.objects.get(isbn=request.data['book'])

        if(request.data['add'] == 'true'):
            if(book.stock == 0):
                return Response({
                    'error': True,
                    'message': 'Não há estoque deste livro!'
                }, status=status.HTTP_409_CONFLICT)
            purchase_item = PurchaseItem(purchase=purchase, book=book)
            purchase_item.save()
            purchase.total = purchase.total + book.price
            purchase.save()
            return Response({
                'error': False,
                'message': 'Livro adicionado ao carrinho com sucesso!'
            }, status=status.HTTP_201_CREATED)
        
        if(request.data['add'] == 'false'):
            purchase_item = PurchaseItem.objects.get(purchase=purchase, book=book)
            purchase.total = purchase.total - book.price
            purchase_item.delete()
            purchase.save()
            return Response({
                'error': False,
                'message': 'Livro removido do carrinho com sucesso!'
            }, status=status.HTTP_201_CREATED)

    def delete(self, request):
        user = User.objects.get(id=request.data['user'])
        purchase = Purchase.objects.get(id=request.data['id'])
        purchase.delete()
        user.cart = None
        user.save()
        return Response({
            'error': False,
            'message': 'Carrinho excluído com sucesso!'
        }, status=status.HTTP_201_CREATED)