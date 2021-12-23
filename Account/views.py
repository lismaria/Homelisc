from django.shortcuts import render,redirect
from django.http import HttpResponse

# Create your views here.

def account_view(request):
    return render(request,"Account/account.html")

def signup_view(request):
    return HttpResponse("SIGNUP")

def login_view(request):
    return HttpResponse("LOGOUT")