from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import HomeView, ShopView, ProductDetailView, LoginView, RegistrationView,\
                   Search, AddToCartView, DeleteFromCartView, LogoutView, CheckoutView, \
                   MakeOrderView

urlpatterns = [
    path('', HomeView.as_view(), name="homepage"),
    path('shop/category/<url>/', ShopView.as_view(), name="shop"),
    path('shop/<slug:slug>/', ProductDetailView.as_view(), name="detail"),

    path('search/', Search.as_view(), name="search"),
    path('add-to-cart/<slug:slug>', AddToCartView.as_view(), name="add_to_cart"),
    path('del-from-cart/<slug:slug>', DeleteFromCartView.as_view(), name="del_from_cart"),
    path('checkout/', CheckoutView.as_view(), name="checkout"),
    path('make-order/', MakeOrderView.as_view(), name='make_order'),

    path('login/', LoginView.as_view(), name="sign_in"),
    path('logout/', LogoutView.as_view(), name="sign_out"),
    path('registration/', RegistrationView.as_view(), name="sign_up"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
