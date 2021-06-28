from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.views import View

from .forms import LoginForm, RegistrationForm, OrderForm
from .models import Category, ProductLine, Section, Product, Cart, CartProduct, Sizes
from .utils import recalc_cart


class HomeView(View):

    def get(self, request, *args, **kwargs):
        category = Category.objects.all()
        line = ProductLine.objects.all()
        section = Section.objects.all()
        product = Product.objects.all()

        topsale = Product.objects.filter(saleProduct="0.3").first()
        topproduct = product[:6]

        context = {
            'category': category, 'line': line, 'section': section,
            'product': product, 'sale': topsale, 'top': topproduct
        }
        if not request.user.is_anonymous:
            cart = Cart.objects.filter(user=request.user, in_order=False).first()
            if not cart:
                cart = Cart.objects.create(user=request.user)
            context.update({'cart': cart})

        return render(request, 'shop/home.html', context)


class ShopView(View):

    def get(self, request, url, *args, **kwargs):
        category = Category.objects.all()
        line = ProductLine.objects.all()
        section = Section.objects.all()
        product = Product.objects.filter(Q(productLine__urlProductLine=url) | Q(category__url=url) |
                                         Q(category__url__icontains=url))

        if url == 'all':
            product = Product.objects.all()

        if url == 'sale':
            product = Product.objects.filter(~Q(saleProduct="0.0"))

        context = {
            'category': category, 'line': line, 'section': section,
            'product': product
        }
        if not request.user.is_anonymous:
            cart = Cart.objects.filter(user=request.user, in_order=False).first()
            if not cart:
                cart = Cart.objects.create(user=request.user)
            context.update({'cart': cart})

        return render(request, 'shop/shops.html', context)


class ProductDetailView(View):

    def get(self, request, slug):
        section = Section.objects.all()
        category = Category.objects.all()
        product = Product.objects.get(id=slug)

        context = {
            'pr': product, 'section': section, 'category': category
        }

        if not request.user.is_anonymous:
            cart = Cart.objects.filter(user=request.user, in_order=False).first()
            if not cart:
                cart = Cart.objects.create(user=request.user)
            context.update({'cart': cart})

        return render(request, 'shop/detail.html', context)


class Search(View):

    def get(self, request):
        product = Product.objects.filter(Q(nameProduct__icontains=self.request.GET.get("searched")) |
                                         Q(productLine__nameProductLine__icontains=self.request.GET.get("searched")))
        section = Section.objects.all()
        category = Category.objects.all()
        line = ProductLine.objects.all()
        context = {
            'category': category, 'line': line, 'section': section,
            'product': product
        }
        if not request.user.is_anonymous:
            cart = Cart.objects.filter(user=request.user, in_order=False).first()
            if not cart:
                cart = Cart.objects.create(user=request.user)
            context.update({'cart': cart})

        return render(request, 'shop/search.html', context)


class AddToCartView(View):

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        user = User.objects.get(username=request.user)
        cart = Cart.objects.get(user=request.user, in_order=False)
        product = Product.objects.filter(id=product_slug).first()
        size = Sizes.objects.filter(id=self.request.GET['productSize']).first()
        qty = self.request.GET['productQty']

        cart_product = CartProduct.objects.create(
            user=user, cart=cart, qty=qty, sizesProduct=size, products=product
        )

        cart.products.add(cart_product)
        recalc_cart(cart)
        messages.add_message(request, messages.INFO, "Товар успешно добавлен")
        return HttpResponseRedirect('../shop/' + str(product_slug))


class DeleteFromCartView(View):

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        cart = Cart.objects.get(user=request.user, in_order=False)
        cart_product = CartProduct.objects.filter(id=product_slug).first()

        cart_product.delete()
        messages.add_message(request, messages.INFO, "Товар успешно удален")
        recalc_cart(cart)
        return HttpResponseRedirect('/')


class CheckoutView(View):

    def get(self, request, *args, **kwargs):
        cart = Cart.objects.get(user=request.user, in_order=False)
        form = OrderForm(request.POST or None)
        context = {
            'cart': cart, 'form': form
        }
        return render(request, 'shop/checkout.html', context)


class MakeOrderView(View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = User.objects.get(username=request.user)
        cart = Cart.objects.get(user=request.user, in_order=False)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.country_choices = form.cleaned_data['country_choices']
            new_order.region = form.cleaned_data['region']
            new_order.locality = form.cleaned_data['locality']
            new_order.postcode = form.cleaned_data['postcode']
            new_order.phone = form.cleaned_data['phone']
            new_order.email_address = form.cleaned_data['email_address']
            new_order.buying_type = form.cleaned_data['buying_type']
            new_order.save()
            cart.in_order = True
            cart.save()
            new_order.cart = cart
            new_order.save()
            messages.add_message(request, messages.INFO, 'Спасибо за ваш заказ!')
            return HttpResponseRedirect('/')
        messages.add_message(request, messages.ERROR, 'Произошла ошибка! Попробуйте еще раз!')
        return HttpResponseRedirect('/checkout/')


class LogoutView(View):

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return redirect('/')


class LoginView(View):

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        context = {'form': form}
        return render(request, 'shop/errorAuthentication.html', context)


class RegistrationView(View):

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()

            User.objects.create_user(new_user)

            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/')
        context = {'form': form}
        return render(request, 'shop/errorAuthentication.html', context)


