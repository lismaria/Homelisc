from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def home(request):
    return HttpResponse("Home")

def search(request):
    return render(request,"search-component.html")

def wishlist(request):
    return HttpResponse("Wishlist")