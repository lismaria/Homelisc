from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request,'home.html')

def search(request):
    return render(request,"search-component.html")

def wishlist(request):
    return render(request,"wishlist.html")