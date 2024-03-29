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
    path('get/ajax/shop/insights/',views.shop_insights, name="shop-insights"),
    path('post/ajax/shop/update/',views.shop_update, name="shop-update"),
    path('post/ajax/item/add/',views.item_add, name="item-add"),
    path('post/ajax/item/edit/',views.item_edit, name="item-edit"),
    path('post/ajax/item/delete/',views.item_delete, name="item-delete"),
    path('post/ajax/itemimg/delete/',views.itemimg_delete, name="itemimg-delete"),
    path('post/ajax/vendor/reply/',views.vendor_reply, name="vendor-reply"),
    path('post/ajax/vendor/heart/',views.vendor_heart, name="vendor-heart"),
]

# path('shop', views.menu_view, name='shop'),
# re_path('shop/'+r'(?P<shop_idd>[01])',views.shop,name="shop")
# re_path(r'[0-9]+\/(?P<shop_slug>[\w-]+)',views.shop,name="shop")