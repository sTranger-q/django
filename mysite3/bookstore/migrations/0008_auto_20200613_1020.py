# Generated by Django 2.2.12 on 2020-06-13 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0007_auto_20200613_1014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(default='', max_length=50, unique=True, verbose_name='书名'),
        ),
    ]
