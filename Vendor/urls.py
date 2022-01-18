from django.urls import path,re_path
from . import views

app_name = "vendor"

urlpatterns = [
    path('', views.vendor_view, name='vendor'),
    path('review', views.review_view, name="review"),
]