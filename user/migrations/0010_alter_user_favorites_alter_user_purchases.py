# Generated by Django 4.2.4 on 2023-10-09 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0010_merge_20231002_1338'),
        ('user', '0009_purchase_user_alter_user_favorites_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='favorites',
            field=models.ManyToManyField(blank=True, through='user.UserFavorites', to='book.book'),
        ),
        migrations.AlterField(
            model_name='user',
            name='purchases',
            field=models.ManyToManyField(blank=True, related_name='purchases', through='user.UserPurchase', to='user.purchase'),
        ),
    ]
