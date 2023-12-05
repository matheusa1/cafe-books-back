from django.shortcuts import render
from .models import Book, Category, BookCategory, Author, BookAuthor, BestBooks
from .api.serializers import BookSerializer, CategorySerializer, BookCategorySerializer, AuthorSerializer, BestBooksSerializer
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
        if (user.type != 'admin'):
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
        if user.type != 'admin':
            return Response({
                'error': True,
                'message': 'Você não tem permissão para atualizar livros!'
            }, status=status.HTTP_401_UNAUTHORIZED)

        try:
            book = Book.objects.get(isbn=request.data['isbn'])
        except Book.DoesNotExist:
            return Response({
                'error': True,
                'message': 'Livro não encontrado!'
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Limpe todos os autores existentes associados ao livro
            book.author.clear()

            # Adicione os novos autores com base em request.data['author']
            for author_name in request.data['author']:
                try:
                    author = Author.objects.get(name=author_name)
                except Author.DoesNotExist:
                    return Response({
                        'error': True,
                        'message': f'O autor "{author_name}" não existe!'
                    }, status=status.HTTP_409_CONFLICT)

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
        if (user.type != 'admin'):
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
        if (user.type != 'admin'):
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
        if (user.type != 'admin'):
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
        if (user.type != 'admin'):
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
        if (user.type != 'admin'):
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
        if (user.type != 'admin'):
            return Response({
                'error': True,
                'message': 'Você não tem permissão para atualizar categorias!'
            }, status=status.HTTP_401_UNAUTHORIZED)
        category = Category.objects.get(
            name=request.data['name'], image=request.data['image'])
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
        if (user.type != 'admin'):
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


class BestSellersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        book = Book.objects.all().order_by('-sales')[:20]
        serializer = BookSerializer(book, many=True)
        return Response(serializer.data)


class BestBooksAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bestbooks = BestBooks.objects.all()
        serializer = BestBooksSerializer(bestbooks, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        if (user.type != 'admin'):
            return Response({
                'error': True,
                'message': 'Você não tem permissão para cadastrar livros!'
            }, status=status.HTTP_401_UNAUTHORIZED)
        bestbooks = BestBooks.objects.all()
        if (bestbooks.count() >= 4):
            return Response({
                'error': True,
                'message': 'Você já cadastrou 4 livros!'
            }, status=status.HTTP_401_UNAUTHORIZED)
        serializer = BestBooksSerializer(data=request.data)
        if (BestBooks.objects.filter(book=request.data['book']).exists()):
            return Response({
                'error': True,
                'message': 'Este livro já está cadastrado nos melhores!',
                'type': 'book'
            }, status=status.HTTP_409_CONFLICT)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'error': False,
                'message': 'Livro cadastrado com sucesso!'
            }, status=status.HTTP_201_CREATED)

        if serializer.errors:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        user = request.user
        if (user.type != 'admin'):
            return Response({
                'error': True,
                'message': 'Você não tem permissão para atualizar livros!'
            }, status=status.HTTP_401_UNAUTHORIZED)
        bestbooks = BestBooks.objects.get(book=request.data['book'])
        serializer = BestBooksSerializer(bestbooks, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'error': False,
                'message': 'Livro atualizado com sucesso!'
            }, status=status.HTTP_201_CREATED)
        if serializer.errors:
            if (request.data['book'] == '' or request.data['call'] == '' or request.data['subtext'] == '' or request.data['image_url'] == ''):
                return Response({
                    'error': True,
                    'message': 'Todos os campos são obrigatórios!'
                }, status=status.HTTP_409_CONFLICT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        if (user.type != 'admin'):
            return Response({
                'error': True,
                'message': 'Você não tem permissão para excluir livros!'
            }, status=status.HTTP_401_UNAUTHORIZED)
        bestbooks = BestBooks.objects.filter(book=request.data['book'])
        try:
            bestbooks.delete()
        except:
            for bestbooks in BestBooks.objects.all():
                bestbooks.delete()
        return Response({
            'error': False,
            'message': 'Livro excluído com sucesso!'
        }, status=status.HTTP_200_OK)


class BiggestPromotionsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        books_with_promotions = Book.objects.exclude(
            promotional_price__isnull=True
        ).order_by('promotional_price')[:10]

        books_with_discounts = []
        for book in books_with_promotions:
            discount_percentage = f'{round((1 - (book.promotional_price / book.price)) * 100)}%'
            books_with_discounts.append({
                'book': BookSerializer(book).data,
                'discount_percentage': discount_percentage
            })

        if books_with_discounts:
            return Response(books_with_discounts)
        else:
            return Response({
                'message': 'Não há livros com desconto disponível.'
            }, status=status.HTTP_404_NOT_FOUND)
