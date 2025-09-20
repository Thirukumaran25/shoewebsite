from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('contact/',views.contact, name='contact'),
    path("thanks/", views.thanks_view, name="enquiry_thanks"),
    path('about/',views.about, name='about'),

    path('men/',views.mens, name='men'),
    path('kids/',views.kids, name='kids'),
    path('women/',views.womens, name='women'),
    path('women/<int:pk>/',views.productdetail, name='productdetail'),
    path('men/<int:pk>/',views.menproductdetail, name='productdetail2'),
    path('kids/<int:pk>/',views.kidproductdetail, name='productdetail3'),
    
    path('login/',views.user_login, name='login'),
    path("register/", views.register_view, name="register"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    
    path('cart/', views.cart, name='cart'),
    # path('cart/', views.cart_view, name='cart'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/cart/', views.checkout_from_cart, name='checkout_from_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    
    # path('checkout1/', views.checkout_view1, name='checkout1'),
    path('checkout/<int:product_id>/', views.checkout_view, name='checkout'),
    path('order-success/<int:order_id>/', views.order_success_view, name='order_success'),
    path('track/<int:order_id>/', views.order_track_view, name='order_track'),
]