from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Section(models.Model):
    nameSection = models.CharField(max_length=64, verbose_name='Название раздела')
    shortName = models.CharField(max_length=3, verbose_name='Аббревиатура раздела')

    def __str__(self):
        return self.nameSection

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'


class Category(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name='Раздел')
    nameCategory = models.CharField(max_length=64, verbose_name='Название категории')
    url = models.SlugField(max_length=32, unique=True)

    def __str__(self):
        return str(self.section.shortName) + ' | ' + str(self.nameCategory)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class ProductLine(models.Model):
    nameProductLine = models.CharField(max_length=64, verbose_name='Название линейки(коллекции)')
    photoProductLine = models.ImageField(upload_to='images/lines/', verbose_name='Логотип линейки')
    urlProductLine = models.SlugField(max_length=12, unique=True)

    def __str__(self):
        return self.nameProductLine

    class Meta:
        verbose_name = 'Линейку'
        verbose_name_plural = 'Линейки'


class Sizes(models.Model):
    sizesProduct = models.CharField(max_length=24, verbose_name="Размер товара")

    def __str__(self):
        return self.sizesProduct

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория товара')
    productLine = models.ForeignKey(ProductLine, on_delete=models.CASCADE, verbose_name='Линейка')
    nameProduct = models.CharField(max_length=64, verbose_name='Наименование товара')
    sizesProduct = models.ManyToManyField(Sizes, verbose_name='Доступные размеры')
    photoProduct = models.ImageField(blank=True, upload_to='images/products/', verbose_name='Фото товара')
    priceProduct = models.PositiveIntegerField(help_text='руб.', verbose_name='Цена продукта')
    saleProduct = models.FloatField(max_length=4, default=0.0, verbose_name='Скидка на товар')

    def __str__(self):
        return self.nameProduct

    def price(self):
        return float(self.priceProduct) - (float(self.priceProduct) * self.saleProduct)

    def sale(self):
        return int(self.saleProduct * 100.0)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class CartProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, verbose_name='Корзина')
    products = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    sizesProduct = models.ForeignKey(Sizes, default='L', on_delete=models.CASCADE, verbose_name='размер')
    qty = models.PositiveIntegerField(default=1, verbose_name='Количество')
    final_price = models.DecimalField(default=0.0, max_digits=9, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return self.products.nameProduct

    def save(self, *args, **kwargs):
        self.final_price = float(self.qty) * self.products.price()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Товар для корзины'
        verbose_name_plural = 'Товары для корзины'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Покупатель')
    products = models.ManyToManyField(CartProduct, blank=True, verbose_name='Товары', related_name='product')
    totalPrice = models.DecimalField(default=0.0, max_digits=9, decimal_places=2, help_text='руб.',
                                     verbose_name='Итоговая цена')
    in_order = models.BooleanField(default=False, verbose_name='Корзина готова')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class Order(models.Model):

    COUNTRY_RUS = 'russia'
    COUNTRY_UKR = 'ukraine'
    COUNTRY_BEL = 'belarus'
    COUNTRY_KAZ = 'kazakhstan'

    COUNTRY_CHOICES = (
        (COUNTRY_RUS, 'Россия'),
        (COUNTRY_UKR, 'Украина'),
        (COUNTRY_BEL, 'Беларусь'),
        (COUNTRY_KAZ, 'Казахстан')
    )

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_DELIVERY, 'Доставка')
    )

    customer = models.ForeignKey(User, verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, null=True, blank=True)

    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    country_choices = models.CharField(max_length=64, verbose_name='Страна',
                                       choices=COUNTRY_CHOICES, default=COUNTRY_RUS)
    region = models.CharField(max_length=64, default='Московская область', verbose_name='Область')
    locality = models.CharField(max_length=64, default='Москва', verbose_name='Город/Поселок')
    postcode = models.IntegerField(default=000000, verbose_name='Почтовый код')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email_address = models.CharField(max_length=64, verbose_name='Адрес', null=True, blank=True)

    buying_type = models.CharField(max_length=100, verbose_name='Тип заказа',
                                   choices=BUYING_TYPE_CHOICES, default=BUYING_TYPE_SELF)

    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        self.totalPrice = self.cart.totalPrice
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
