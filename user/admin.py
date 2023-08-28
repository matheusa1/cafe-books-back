from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        ('User information',{
            'fields':['type','id','name','email','password','birth_date','phone','sex','address']
        })
    ]
    list_display = ('type','id','name','email','password','birth_date','phone','sex','address')

admin.site.register(User)

# Register your models here.
