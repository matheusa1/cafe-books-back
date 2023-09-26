from rest_framework import viewsets
from book.api import serializers
from book import models


class BookViewsSet(viewsets.ModelViewSet):
    serializer_class = serializers.BookSerializer
    queryset = models.Book.objects.all()
    
class CategoryViewsSet(viewsets.ModelViewSet):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()    

class BookCategoryViewsSet(viewsets.ModelViewSet):
    serializer_class = serializers.BookCategorySerializer
    queryset = models.BookCategory.objects.all()

class AuthorViewsSet(viewsets.ModelViewSet):
    serializer_class = serializers.AuthorSerializer
    queryset = models.Author.objects.all()    