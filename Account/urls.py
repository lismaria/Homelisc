from django.urls import path,re_path
from . import views

app_name = "account"

urlpatterns = [
    path('', views.account_view, name="account"),
    path('signup', views.signup_view, name = "signup"),
    path('logout', views.logout_view, name = "logout"),
    re_path('login/'+r'(?P<login_as>[01])', views.login_view, name = "login"),
]