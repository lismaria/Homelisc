from django.urls import path,re_path
from . import views

app_name = "vendor"

urlpatterns = [
    path('', views.shop_view, name='shop'),
    path('review', views.review_view, name="review"),
    path('menu', views.menu_view, name='menu'),
]