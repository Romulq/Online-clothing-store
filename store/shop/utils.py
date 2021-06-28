from django.db import models

''' Подсчет суммы заказа '''


def recalc_cart(cart):
    cart_data = cart.products.aggregate(models.Sum('final_price'))
    if cart_data.get('final_price__sum'):
        cart.totalPrice = cart_data['final_price__sum']
    else:
        cart.totalPrice = 0
    cart.save()
