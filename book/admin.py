from django.contrib import admin
from .models import Book, Category, BookCategory, Author

class BookAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Book Information', {'fields': ['isbn', 'title', 'author', 'publisher', 'country', 'language', 'year', 'pages', 'price', 'stock', 'category']}),
    ]
    list_display = ('isbn', 'title', 'author', 'publisher', 'country', 'language', 'year', 'pages', 'price', 'stock', 'category')

class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Category Information', {'fields': ['name', 'image_url']}),
    ]
    list_display = ('name', 'image_url')

class BookCategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Book Category Information', {'fields': ['book', 'category']}),
    ]
    list_display = ('book', 'category')

class AuthorAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Author Information', {'fields': ['name', 'image_url']}),
    ]
    list_display = ('name', 'image_url')


admin.site.register(Book)
admin.site.register(Category)
admin.site.register(BookCategory)
admin.site.register(Author)


# Register your models here.
