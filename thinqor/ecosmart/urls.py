from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.navbar, name='navbar'),
    path('products', views.products, name='products'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('home', views.home, name='home'),
    path('product_cart/<int:user_id>/', views.product_cart, name='product_cart'),
    path('product_book/<int:user_id>/', views.product_book, name='product_book'),
    path('booked_products', views.booked_products, name='booked_products'),
    path('shipping_address', views.shipping_address, name='shipping_address'),
    path('checkout', views.checkout, name='checkout'),
    path('cart_view/<int:user_id>/', views.cart_view, name='cart_view'),
    path('get_cart_item_count', views.get_cart_item_count, name='get_cart_item_count'),
    path('checkout_cart', views.checkout_cart, name='checkout_cart'),
    path('remove_item/<int:id>/', views.remove_item, name='remove_item'),
    path('payment', views.payment, name='payment'),
    path('paymentdone', views.paymentdone, name='paymentdone')
    ]