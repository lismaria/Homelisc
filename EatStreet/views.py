from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def home(request):
    if not request.user.is_authenticated:
        return render(request,'home.html',{'food':'chocolates'})
    elif (request.user.is_authenticated and request.user.is_vendor == True):
        return render(request,'Vendor/vendor.html',{'food':'chocolates'})
    else:
        return render(request,'home.html',{'food':'chocolates'})

def search(request):
    return render(request,"search.html")

def wishlist(request):
    return render(request,"wishlist.html")

def category(request):
    category = request.GET['category']
    return render(request,"category.html",{'category':category})

def product(request):
    return render(request,"product.html")

def shop(request,food):
    return render(request,"shop.html",{'food':food})

def reviews(request):
    return render(request,"reviews.html")
