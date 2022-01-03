from django.shortcuts import render,redirect
from django.http import HttpResponse

# Create your views here.

def account_view(request):
    return render(request,"Account/account.html")

def signup_view(request):
    signup_as = request.GET['as']
    return HttpResponse(signup_as)

def login_view(request):
    login_as = request.GET['as']
    return render(request,"Account/login.html",{'login_as':login_as})