from django.db import models
from book.models import Book

# Create your models here.

class Purchase(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, default=None)
    date = models.DateTimeField(auto_now_add=True)
    total = models.FloatField()
    books = models.ManyToManyField(Book, through='PurchaseItem')

    def __str__(self):
        return self.user.name + ' - ' + str(self.date)
    
class User(models.Model):
    USER_TYPE_CHOICES = (
        ('Admin', 'admin'), 
        ('User', 'user'),
    )

    SEX_CHOICE = (
        ('Masculino', 'masculino'),
        ('Feminino', 'feminino'),
        ('Outro', 'outro'), 
    )

    type = models.CharField(max_length=5, default='user')
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    sex = models.CharField(max_length=9, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    favorites = models.ManyToManyField(Book, through='UserFavorites', blank=True, null=True)
    purchases = models.ManyToManyField(Purchase, through='UserPurchase', blank=True, related_name='purchases', null=True)

    def __str__(self):
        return self.name

class UserFavorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.name + ' - ' + self.book.title
    

class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()

    def __str__(self):
        return self.purchase.user.name + ' - ' + self.book.title + ' - ' + str(self.quantity) + ' - ' + str(self.price)
    
class UserPurchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.name + ' - ' + self.purchase.user.name + ' - ' + str(self.purchase.date)

