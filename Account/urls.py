from django.urls import path,re_path
from . import views

app_name = "account"

urlpatterns = [
    path('', views.account_view, name="account"),
    path('logout', views.logout_view, name = "logout"),
    re_path('login/'+r'(?P<login_as>[01])', views.login_view, name = "login"),
    re_path('signup/'+r'(?P<signup_as>[01])', views.signup_view, name = "signup"),
]