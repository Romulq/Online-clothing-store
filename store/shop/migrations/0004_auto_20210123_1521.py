# Generated by Django 3.1.5 on 2021-01-23 07:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20210122_2251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.section', verbose_name='Раздел'),
        ),
    ]