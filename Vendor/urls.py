from django.urls import path,re_path
from . import views

app_name = "vendor"

urlpatterns = [
    path('', views.home, name='home'),
    path('<slug:id>/<slug:slug>/menu', views.menu_view, name='menu'),
    path('<slug:id>/<slug:slug>/review', views.review_view, name="review"),
    path('register-shop',views.register_shop,name="register-shop"),
    path('<slug:id>/<slug:slug>/shop',views.shop_view,name="shop"),
    path('post/ajax/vendor/update/',views.vendor_update,name="vendor-update"),
    path('post/ajax/shop/update/',views.shop_update, name="shop_update")
]

# path('shop', views.menu_view, name='shop'),
# re_path('shop/'+r'(?P<shop_idd>[01])',views.shop,name="shop")
# re_path(r'[0-9]+\/(?P<shop_slug>[\w-]+)',views.shop,name="shop")