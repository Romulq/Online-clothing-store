# Generated by Django 3.1.5 on 2021-06-09 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_auto_20210609_1824'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='sizesProduct',
        ),
        migrations.AddField(
            model_name='product',
            name='sizesProduct',
            field=models.ManyToManyField(to='shop.Sizes', verbose_name='Доступные размеры'),
        ),
    ]
