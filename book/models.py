from django.db import models

# Create your models here.

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

    def __str__(self):
        return self.title