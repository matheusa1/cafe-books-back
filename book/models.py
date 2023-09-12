from django.db import models

# Create your models here.

class Category(models.Model):    
    name = models.CharField(max_length=255)
    image_url = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name
    
class Book(models.Model):
    isbn = models.CharField(max_length=45, primary_key=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    year = models.IntegerField()
    pages = models.IntegerField()
    price = models.FloatField()
    stock = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    