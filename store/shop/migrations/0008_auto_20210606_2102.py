# Generated by Django 3.1.5 on 2021-06-06 13:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_auto_20210606_1537'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='product',
            new_name='products',
        ),
        migrations.RemoveField(
            model_name='product',
            name='materialProduct',
        ),
        migrations.RemoveField(
            model_name='product',
            name='quantityProduct',
        ),
    ]