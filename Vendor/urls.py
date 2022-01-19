from django.urls import path,re_path
from . import views

app_name = "vendor"

urlpatterns = [
    path('', views.shop_view, name='shop'),
    path('reviews', views.reviews_view, name="reviews"),
    path('menu', views.menu_view, name='menu'),
    path('register-shop',views.register_shop,name="register-shop")
]