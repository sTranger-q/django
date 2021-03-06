# Generated by Django 2.2.12 on 2020-06-13 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookstore', '0008_auto_20200613_1020'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='是否活跃'),
        ),
        migrations.AddField(
            model_name='book',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='是否活跃'),
        ),
    ]
