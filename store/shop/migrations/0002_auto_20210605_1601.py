# Generated by Django 3.1.5 on 2021-06-05 08:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sizes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sizesProduct', models.CharField(max_length=24, verbose_name='Размер товара')),
            ],
            options={
                'verbose_name': 'Размер',
                'verbose_name_plural': 'Размеры',
            },
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Товар', 'verbose_name_plural': 'Товары'},
        ),
        migrations.RemoveField(
            model_name='productline',
            name='aboutProductLine',
        ),
        migrations.AlterField(
            model_name='cart',
            name='countProduct',
            field=models.PositiveSmallIntegerField(help_text='руб.', verbose_name='Цена товара'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.product', verbose_name='Категория товара'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='summPrice',
            field=models.PositiveIntegerField(help_text='руб.', verbose_name='Цена зв единицу товара'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Покупатель'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.category', verbose_name='Категория товара'),
        ),
        migrations.AlterField(
            model_name='product',
            name='nameProduct',
            field=models.CharField(max_length=64, verbose_name='Наименование товара'),
        ),
        migrations.AlterField(
            model_name='product',
            name='photoProduct',
            field=models.ImageField(blank=True, upload_to='images/products/%Y/%m/%d/', verbose_name='Фото товара'),
        ),
        migrations.AlterField(
            model_name='productline',
            name='photoProductLine',
            field=models.ImageField(upload_to='images/lines/', verbose_name='Логотип линейки'),
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
