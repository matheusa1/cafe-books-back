from rest_framework import serializers
from book import models


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Book
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'


class BookCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BookCategory
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Author
        fields = '__all__'


class BestBooksSerializer(serializers.ModelSerializer):
    book_details = BookSerializer(source='book', read_only=True)

    class Meta:
        model = models.BestBooks
        fields = '__all__'
