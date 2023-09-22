from django.db import models

# Create your models here.
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

    def __str__(self):
        return self.email