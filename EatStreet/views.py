from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request,'home.html',{'food':'vada-pav'})

def search(request):
    return render(request,"search.html")

def wishlist(request):
    return render(request,"wishlist.html")

def cuisine(request):
    cuisine = request.GET['cuisine']
    return render(request,"top-cuisine.html",{'cuisine':cuisine})