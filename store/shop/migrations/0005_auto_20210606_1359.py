# Generated by Django 3.1.5 on 2021-06-06 05:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20210606_1349'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='sale',
            new_name='saleProduct',
        ),
    ]
