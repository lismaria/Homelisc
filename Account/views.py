from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def signup_view(request):
    return HttpResponse("SIGNUP")

def login_view(request):
    return HttpResponse("LOGIN")

def logout_view(request):
    return HttpResponse("LOGOUT")