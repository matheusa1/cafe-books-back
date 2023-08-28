from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Book Information', {'fields': ['isbn', 'title', 'author', 'publisher', 'country', 'language', 'year', 'pages', 'price', 'stock']}),
    ]
    list_display = ('isbn', 'title', 'author', 'publisher', 'country', 'language', 'year', 'pages', 'price', 'stock')


admin.site.register(Book)


# Register your models here.
