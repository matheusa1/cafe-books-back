from django.shortcuts import render
from .models import User, Purchase, PurchaseItem, UserFavorites, UserPurchase
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

from rest_framework_simplejwt.views import TokenObtainPairView
from user.api.serializers import CustomTokenObtainPairSerializer
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
        if("type" not in request.data):
            request.data['type'] = 'User'
        elif(request.data['type'] == 'admin'):
            if("adminPassword" not in request.data or request.data['adminPassword'] != 'admindocafebooks'):
                return Response({
                    'error': True,
                    'message': 'Senha administrativa incorreta!'
                }, status=status.HTTP_409_CONFLICT)
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
            if not request.data.get('name') or not request.data.get('email') or not request.data.get('password'):
                return Response({
                    'error': True,
                    'message': 'Todos os campos são obrigatórios!'
                }, status=status.HTTP_409_CONFLICT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class PurchaseAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        purchase = Purchase.objects.all()
        serializer = PurchaseSerializer(purchase, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        user = request.user
        
        def clear_cart(user):
            user.cart = None
            user.save()

        if not user:
            return Response({'error': True, 'message': 'Usuário não informado!'}, status=status.HTTP_409_CONFLICT)

        try:
            user = User.objects.get(id=user.id)
        except User.DoesNotExist:
            return Response({'error': True, 'message': 'Usuário não encontrado!'}, status=status.HTTP_404_NOT_FOUND)

        if not hasattr(user, 'cart') or user.cart is None:
            return Response({'error': True, 'message': 'Carrinho vazio!'}, status=status.HTTP_409_CONFLICT)

        purchase_items = PurchaseItem.objects.filter(purchase=user.cart)
        print(purchase_items)

        new_purchase = Purchase(user=user, status='Pendente', total=user.cart.total, address=request.data.get('address', user.address or ''))
        new_purchase.save()

        for item in purchase_items:
            print(item.book.stock)
            if item.book.stock < item.quantity:
                new_purchase.delete()
                return Response({'error': True, 'message': f'Estoque insuficiente para o livro {item.book.title}'}, status=status.HTTP_409_CONFLICT)

            item.book.stock -= item.quantity
            item.book.save()
            
            purchase_item =  PurchaseItem.objects.create(purchase=new_purchase, book=item.book, price=item.price, quantity=item.quantity)
            purchase_item.save()

        clear_cart(user)

        user_purchase = UserPurchase.objects.create(user=user, purchase=new_purchase)
        user_purchase.save()

        return Response({'error': False, 'message': 'Compra realizada com sucesso!'}, status=status.HTTP_201_CREATED)
        
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
        }, status=status.HTTP_200_OK)
    
class PurchaseWithoutCartAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        if(not request.user):
            return Response({
                'error': True,
                'message': 'Usuário não informado!'
            }, status=status.HTTP_409_CONFLICT)
        user = request.user
        purchase = Purchase(user=user, status='Pendente', total=0.0)
        purchase.save()
        user_purchase = UserPurchase(user=user, purchase=purchase)
        user_purchase.save()
        book = Book.objects.get(isbn=request.data['book'])
        purchase_item = PurchaseItem(purchase=purchase, book=book)
        purchase_item.price = book.price
        purchase_item.quantity = request.data['quantity']
        purchase_item.save()
        purchase.total = purchase_item.price * purchase_item.quantity
        book.stock = book.stock - 1
        book.save()
        purchase.save()

        return Response({
            'error': False,
            'message': 'Compra criada com sucesso!'
        }, status=status.HTTP_201_CREATED)
        

class FavoritesAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        books = user.favorites.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        if(not request.user):
            return Response({
                'error': True,
                'message': 'Usuário não informado!'
            }, status=status.HTTP_409_CONFLICT)
        user = request.user

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
        user =  request.user
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
        }, status=status.HTTP_200_OK)

class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            user = request.user
            
            if not hasattr(user, 'cart') or user.cart is None:
                return Response({
                    'error': True,
                    'message': 'Carrinho vazio!'
                }, status=status.HTTP_409_CONFLICT)
            
            serializer = PurchaseSerializer(user.cart)
            return Response(serializer.data)

        except User.DoesNotExist:
            return Response({'error': True, 'message': 'Usuário não encontrado!'}, status=status.HTTP_404_NOT_FOUND)
        

    def post(self, request):
        try:
            user = request.user
            
            if not hasattr(user, 'cart') or user.cart is None:
                purchase = Purchase(user=user, status='Pendente', total=0.0)
                purchase.save()
                user.cart = purchase
                user.save()
            else:
                purchase = user.cart
            
            if not request.data.get('book'):
                return Response({'error': True, 'message': 'Nenhum livro informado!'}, status=status.HTTP_409_CONFLICT)

            book = Book.objects.get(isbn=request.data['book'])

            if request.data.get('add', '').lower() == 'true':                
            
                quantity_to_set = int(request.data.get('quantity', 1)) 
                
                if quantity_to_set <= 0:
                    return Response({'error': True, 'message': 'Quantidade inválida!'}, status=status.HTTP_400_BAD_REQUEST)
                
                if quantity_to_set > book.stock:
                    return Response({'error': True, 'message': 'Quantidade indisponível no estoque!'}, status=status.HTTP_400_BAD_REQUEST)
                
                purchase_item, created = PurchaseItem.objects.get_or_create(purchase=purchase,book=book,defaults={'price': book.price,'quantity': 1})           
                
                if created:
                    purchase_item.quantity = quantity_to_set
                else:
                    purchase.total += book.price * (quantity_to_set - purchase_item.quantity)
                    purchase_item.quantity = quantity_to_set

                purchase_item.price = book.price
                purchase_item.save()
                purchase.save()
                purchase.recalculate_total()

                return Response({'error': False, 'message': f'{quantity_to_set} cópias do livro configuradas no carrinho com sucesso!'}, status=status.HTTP_201_CREATED)
                
            elif request.data.get('add', '').lower() == 'false':
                purchase_item = PurchaseItem.objects.filter(purchase=purchase, book=book).first()

                if not purchase_item:
                    return Response({'error': True, 'message': 'Este livro não está no carrinho!'}, status=status.HTTP_404_NOT_FOUND)
                
                quantity_to_remove = int(request.data.get('quantity', 1))

                if purchase_item.quantity <= quantity_to_remove:
                    purchase_item.delete()
                else:
                    purchase_item.quantity -= quantity_to_remove
                    purchase_item.save()

                purchase.recalculate_total()

                return Response({'error': False, 'message': f'{quantity_to_remove} Livros removidos do carrinho com sucesso!'}, status=status.HTTP_201_CREATED)

            return Response({'error': True, 'message': 'Valor inválido para o campo "add".'}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({'error': True, 'message': 'Usuário não encontrado!'}, status=status.HTTP_404_NOT_FOUND)
        except Book.DoesNotExist:
            return Response({'error': True, 'message': 'Livro não encontrado!'}, status=status.HTTP_404_NOT_FOUND)
           

    def delete(self, request):
        try:
            user = request.user
            purchase = Purchase.objects.get(id=request.data['id'])
            purchase.delete()
            user.cart = None
            user.save()
            return Response({
                'error': False,
                'message': 'Carrinho excluído com sucesso!'
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': True, 'message': 'Usuário não encontrado!'}, status=status.HTTP_404_NOT_FOUND)
        except Purchase.DoesNotExist:
            return Response({'error': True, 'message': 'Carrinho não encontrado!'}, status=status.HTTP_404_NOT_FOUND)
        
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class GetPurchaseByUser(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        purchases = user.purchases.all()
        serializer = PurchaseSerializer(purchases, many=True)
        return Response(serializer.data)
    
class GetRecommended(APIView):
    def get(self,request):
        pass