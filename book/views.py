from django.shortcuts import render
from .models import Book, Category, BookCategory, Author, BookAuthor
from .api.serializers import BookSerializer, CategorySerializer, BookCategorySerializer, AuthorSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status

from rest_framework.permissions import IsAuthenticated


class BookAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        book = Book.objects.all()
        serializer = BookSerializer(book, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        if(user.type != 'admin'):
            return Response({
                'error': True,
                'message': 'Você não tem permissão para cadastrar livros!'
            }, status=status.HTTP_401_UNAUTHORIZED)
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            for categories in request.data['category']:
                if (Category.objects.filter(name=categories).exists() == False):
                    return Response({
                        'error': True,
                        'message': 'Esta categoria não existe!'
                    }, status=status.HTTP_409_CONFLICT)
                category = Category.objects.get(name=categories)
                book = Book.objects.get(isbn=request.data['isbn'])
                book_category = BookCategory(book=book, category=category)
                book_category.save()
            for author in request.data['author']:
                if (Author.objects.filter(name=author).exists() == False):
                    return Response({
                        'error': True,
                        'message': 'Este autor não existe!'
                    }, status=status.HTTP_409_CONFLICT)
                author = Author.objects.get(name=author)
                book = Book.objects.get(isbn=request.data['isbn'])
                book_author = BookAuthor(book=book, author=author)
                book_author.save()
            return Response({
                'error': False,
                'message': 'Livro cadastrado com sucesso!'
            }, status=status.HTTP_201_CREATED)

        if serializer.errors:
            if (Book.objects.get(isbn=request.data['isbn'])):
                return Response({
                    'error': True,
                    'message': 'Este ISBN já está cadastrado!',
                    'type': 'isbn'
                }, status=status.HTTP_409_CONFLICT)
            if (request.data['isbn'] == '' or request.data['title'] == '' or request.data['author'] == '' or request.data['description'] == '' or request.data['category'] == '' or request.data['image'] == '' or request.data['pages'] == '' or request.data['year'] == '' or request.data['publisher'] == '' or request.data['language'] == '' or request.data['price'] == '' or request.data['stock'] == ''):
                return Response({
                    'error': True,
                    'message': 'Todos os campos são obrigatórios!'
                }, status=status.HTTP_409_CONFLICT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        user = request.user
        if(user.type != 'admin'):
            return Response({
                'error': True,
                'message': 'Você não tem permissão para atualizar livros!'
            }, status=status.HTTP_401_UNAUTHORIZED)
        book = Book.objects.get(isbn=request.data['isbn'])
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            for categories in book.category.all():
                if (categories.name not in request.data['category']):
                    book = Book.objects.get(isbn=request.data['isbn'])
                    book_category = BookCategory.objects.get(
                        book=book, category=categories)
                    book_category.delete()
            for categories in request.data['category']:
                category = Category.objects.get(name=categories)
                if (category not in book.category.all()):
                    book = Book.objects.get(isbn=request.data['isbn'])
                    book_category = BookCategory(book=book, category=category)
                    book_category.save()
            for author in book.author.all():
                if (author.name not in request.data['author']):
                    book = Book.objects.get(isbn=request.data['isbn'])
                    book_author = BookAuthor.objects.get(
                        book=book, author=author)
                    book_author.delete()
            for author in request.data['author']:
                if (Author.objects.filter(name=author).exists() == False):
                    return Response({
                        'error': True,
                        'message': 'Este autor não existe!'
                    }, status=status.HTTP_409_CONFLICT)
                author = Author.objects.get(name=author)
                book = Book.objects.get(isbn=request.data['isbn'])
                book_author = BookAuthor(book=book, author=author)
                book_author.save()
            return Response({
                'error': False,
                'message': 'Livro atualizado com sucesso!'
            }, status=status.HTTP_201_CREATED)
        if serializer.errors:
            if (request.data['isbn'] == '' or request.data['name'] == '' or request.data['author'] == '' or request.data['description'] == '' or request.data['category'] == '' or request.data['image'] == '' or request.data['pages'] == '' or request.data['year'] == '' or request.data['publisher'] == '' or request.data['language'] == '' or request.data['price'] == '' or request.data['stock'] == ''):
                return Response({
                    'error': True,
                    'message': 'Todos os campos são obrigatórios!'
                }, status=status.HTTP_409_CONFLICT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        if(user.type != 'admin'):
            return Response({
                'error': True,
                'message': 'Você não tem permissão para excluir livros!'
            }, status=status.HTTP_401_UNAUTHORIZED)
        book = Book.objects.get(isbn=request.data['isbn'])
        book.delete()
        return Response({
            'error': False,
            'message': 'Livro excluído com sucesso!'
        }, status=status.HTTP_200_OK)


class AuthorAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        author = Author.objects.all()
        serializer = AuthorSerializer(author, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        if(user.type != 'admin'):
            return Response({
                'error': True,
                'message': 'Você não tem permissão para cadastrar autores!'
            }, status=status.HTTP_401_UNAUTHORIZED)
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'error': False,
                'message': 'Autor cadastrado com sucesso!'
            }, status=status.HTTP_201_CREATED)

        if serializer.errors:
            if (Author.objects.filter(name=request.data['name']).exists()):
                return Response({
                    'error': True,
                    'message': 'Este autor já está cadastrado!',
                    'type': 'author'
                }, status=status.HTTP_409_CONFLICT)
            if (request.data['name'] == ''):
                return Response({
                    'error': True,
                    'message': 'Todos os campos são obrigatórios!'
                }, status=status.HTTP_409_CONFLICT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        user = request.user
        if(user.type != 'admin'):
            return Response({
                'error': True,
                'message': 'Você não tem permissão para atualizar autores!'
            }, status=status.HTTP_401_UNAUTHORIZED)
        author = Author.objects.get(name=request.data['name'])
        serializer = AuthorSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'error': False,
                'message': 'Autor atualizado com sucesso!'
            }, status=status.HTTP_201_CREATED)
        if serializer.errors:
            if (request.data['name'] == ''):
                return Response({
                    'error': True,
                    'message': 'Todos os campos são obrigatórios!'
                }, status=status.HTTP_409_CONFLICT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        if(user.type != 'admin'):
            return Response({
                'error': True,
                'message': 'Você não tem permissão para excluir autores!'
            }, status=status.HTTP_401_UNAUTHORIZED)
        author = Author.objects.get(name=request.data['name'])
        author.delete()
        return Response({
            'error': False,
            'message': 'Autor excluído com sucesso!'
        }, status=status.HTTP_200_OK)

class CategoryAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        if(user.type != 'admin'):
            return Response({
                'error': True,
                'message': 'Você não tem permissão para cadastrar categorias!'
            }, status=status.HTTP_401_UNAUTHORIZED)
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'error': False,
                'message': 'Categoria cadastrada com sucesso!'
            }, status=status.HTTP_201_CREATED)

        if serializer.errors:
            if (Category.objects.filter(name=request.data['name']).exists()):
                return Response({
                    'error': True,
                    'message': 'Esta categoria já está cadastrada!',
                    'type': 'category'
                }, status=status.HTTP_409_CONFLICT)
            if (request.data['name'] == ''):
                return Response({
                    'error': True,
                    'message': 'Todos os campos são obrigatórios!'
                }, status=status.HTTP_409_CONFLICT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        user = request.user
        if(user.type != 'admin'):
            return Response({
                'error': True,
                'message': 'Você não tem permissão para atualizar categorias!'
            }, status=status.HTTP_401_UNAUTHORIZED)
        category = Category.objects.get(name=request.data['name'], image=request.data['image'])
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'error': False,
                'message': 'Categoria atualizada com sucesso!'
            }, status=status.HTTP_201_CREATED)
        if serializer.errors:
            if (request.data['name'] == '' or request.data['image'] == ''):
                return Response({
                    'error': True,
                    'message': 'Todos os campos são obrigatórios!'
                }, status=status.HTTP_409_CONFLICT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        if(user.type != 'admin'):
            return Response({
                'error': True,
                'message': 'Você não tem permissão para excluir categorias!'
            }, status=status.HTTP_401_UNAUTHORIZED)
        category = Category.objects.get(name=request.data['name'])
        category.delete()
        return Response({
            'error': False,
            'message': 'Categoria excluída com sucesso!'
        }, status=status.HTTP_200_OK)
    