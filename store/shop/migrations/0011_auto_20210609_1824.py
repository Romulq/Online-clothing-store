# Generated by Django 3.1.5 on 2021-06-09 10:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_auto_20210609_1822'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sizesProduct',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='shop.sizes',
                                    verbose_name='размеры'),
        ),
    ]
