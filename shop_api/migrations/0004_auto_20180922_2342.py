# Generated by Django 2.1.1 on 2018-09-22 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_api', '0003_auto_20180922_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
