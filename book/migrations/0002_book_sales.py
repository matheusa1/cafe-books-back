# Generated by Django 4.2.5 on 2023-11-16 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='sales',
            field=models.IntegerField(default=0),
        ),
    ]
