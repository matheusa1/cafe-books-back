from django.db import models
from book.models import Book

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

# Create your models here.

class Purchase(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, default=None)
    date = models.DateTimeField(auto_now_add=True)
    total = models.FloatField()
    books = models.ManyToManyField(Book, through='PurchaseItem')

    def __str__(self):
        return self.user.name + ' - ' + str(self.date)
    
class UserManager(BaseUserManager):
    def create_user(self, email, name, password):
        if not email:
            raise ValueError('Usuário deve ter um e-mail válido!')
        if not name:
            raise ValueError('Usuário deve ter um nome válido!')
        if not password:
            raise ValueError('Usuário deve ter uma senha válida!')
        
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            password=password,
        )
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, name, password):
        user = self.create_user(
            email=self.normalize_email(email),
            name=name,
            password=password,
        )
        user.type = 'admin'
        user.save(using=self._db)
        return user
    
class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('Admin', 'admin'), 
        ('User', 'user'),
    )
    SEX_CHOICE = (
        ('Masculino', 'masculino'),
        ('Feminino', 'feminino'),
        ('Outro', 'outro'), 
    )

    username = None
    type = models.CharField(max_length=5, default='user')
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    sex = models.CharField(max_length=9, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    favorites = models.ManyToManyField(Book, through='UserFavorites', blank=True)
    purchases = models.ManyToManyField(Purchase, through='UserPurchase', blank=True, related_name='purchases')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'password']


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

