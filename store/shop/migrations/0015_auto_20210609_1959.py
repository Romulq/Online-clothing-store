# Generated by Django 3.1.5 on 2021-06-09 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_auto_20210609_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartproduct',
            name='sizesProduct',
            field=models.ForeignKey(default='L', on_delete=django.db.models.deletion.CASCADE, to='shop.sizes', verbose_name='размер'),
        ),
    ]
