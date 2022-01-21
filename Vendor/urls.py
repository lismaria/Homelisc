from django.urls import path,re_path
from . import views

app_name = "vendor"

urlpatterns = [
    path('', views.shop_view, name='home'),
    path('review', views.review_view, name="review"),
    path('menu', views.menu_view, name='menu'),
    path('register-shop',views.register_shop,name="register-shop"),
    # path('shop', views.menu_view, name='shop'),
    re_path('shop/'+r'(?P<shop_idd>[01])',views.shop,name="shop")
    # re_path(r'[0-9]+\/(?P<shop_slug>[\w-]+)',views.shop,name="shop")
]