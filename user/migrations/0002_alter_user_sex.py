# Generated by Django 4.2.4 on 2023-09-21 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.CharField(blank=True, choices=[('Masculino', 'masculino'), ('Feminino', 'feminino'), ('Outro', 'outro')], max_length=9, null=True),
        ),
    ]