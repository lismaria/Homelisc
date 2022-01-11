from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request,'home.html',{'food':'chocolates'})

def search(request):
    return render(request,"search.html")

def wishlist(request):
    return render(request,"wishlist.html")

def category(request):
    category = request.GET['category']
    return render(request,"category.html",{'category':category})

def product(request):
    product = request.GET['product']
    return render(request,"product.html",{'product':product})

def shop(request,food):
    return render(request,"shop.html",{'food':food})
