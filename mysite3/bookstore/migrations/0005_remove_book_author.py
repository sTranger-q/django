# Generated by Django 2.2.12 on 2020-06-13 01:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0004_auto_20200612_1903'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='author',
        ),
    ]
