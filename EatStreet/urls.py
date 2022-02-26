"""EatStreet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, re_path
from django.conf.urls import include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('Vendor.urls',namespace='vendor')),
    path('',views.home,name="home"),
    path('account/', include('Account.urls')),

    path('search/',views.search,name="search"),
    path('wishlist/',views.wishlist,name="wishlist"),
    path('category/',views.category,name="category"),
    path('shop/<slug:id>/<slug:slug>/product/<slug:itemid>',views.product,name="product"),
    path('shop/<slug:id>/<slug:slug>/reviews',views.reviews,name="reviews"),
    path('shop/<slug:id>/<slug:slug>',views.shop,name="shop"),
    path('post/ajax/review/post/',views.review_post,name="review-post"),
    path('post/ajax/add-wishlist/',views.add_wishlist,name="add-wishlist"),
    path('post/ajax/review/like/',views.review_like,name="review-like"),

    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="pswd/password-reset.html", html_email_template_name="pswd/password-reset-email.html"), name="reset_password"), # The reset form asking the email
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="pswd/password-reset-sent.html"), name="password_reset_done"), # Email sent msg
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="pswd/password-reset-form.html"), name="password_reset_confirm"), # The email link to actually set the password
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="pswd/password-reset-complete.html"), name="password_reset_complete"), # Password reset done msg

    path('change_password/',auth_views.PasswordChangeView.as_view(template_name="pswd/password-change.html"), name="password_change"), # The change password form
    path('change_password_complete/',auth_views.PasswordChangeDoneView.as_view(template_name="pswd/password-change-complete.html"), name="password_change_done"), # The change password success msg (name is imp - dont change)

]


urlpatterns+=staticfiles_urlpatterns()
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)