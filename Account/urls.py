from django.urls import path
from . import views

app_name = "account"

urlpatterns = [
    path('', views.account_view, name="account"),
    path('signup/', views.signup_view, name = "signup"),
    path('login/', views.login_view, name = "login")
]