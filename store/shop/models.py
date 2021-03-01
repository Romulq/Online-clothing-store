from django.db import models


class Section(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название раздела')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название категории')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name = 'Раздел')

    def __str__(self):
        return self.name + ' - ' + self.section.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название линейки(коллекции)')
    aboutCompany = models.TextField(blank=True, verbose_name='О линейке')
    image = models.ImageField(upload_to='images/%Y/%m/%d/', verbose_name='Логотип линейки')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Линейка'
        verbose_name_plural = 'Линейки'


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name = 'Категория одежды')
    name = models.CharField(max_length=12, verbose_name='Наименование продукта')
    image = models.ImageField(upload_to='images/%Y/%m/%d/', verbose_name='Изображение продукта')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Линейка')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'