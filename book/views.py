from django.shortcuts import render
from .models import Book, Category, BookCategory
from .api.serializers import BookSerializer, CategorySerializer, BookCategorySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status

class BookAPIView(APIView):
    def get(self, request):
        book = Book.objects.all()
        serializer = BookSerializer(book, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            for categories in request.data['category']:
                category = Category.objects.get(name=categories)
                book = Book.objects.get(isbn=request.data['isbn'])
                book_category = BookCategory(book=book, category=category)
                book_category.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        book = Book.objects.get(isbn=request.data['isbn'])
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            for categories in request.data['category']:
                category = Category.objects.get(name=categories)
                if(category not in book.category.all()):
                    book = Book.objects.get(isbn=request.data['isbn'])
                    book_category = BookCategory(book=book, category=category)
                    book_category.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)