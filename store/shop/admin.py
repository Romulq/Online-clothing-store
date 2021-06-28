from django.contrib import admin
from .models import Section, Category, ProductLine, Product, Sizes, CartProduct, Cart, Order


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ('nameCategory', 'section')
    search_fields = ['nameCategory', 'section__name']


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ('nameProduct', 'id', 'sale', 'price')
    search_fields = ['nameProduct']


class CartAdmin(admin.ModelAdmin):
    model = Cart
    list_display = ('user', 'id', 'in_order', 'totalPrice', )
    readonly_fields = ('totalPrice', )
    search_fields = ['user', 'totalPrice']


class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ('customer',  'id')
    search_fields = ['customer',]


admin.site.register(Section)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductLine)
admin.site.register(Sizes)
admin.site.register(Product, ProductAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)

