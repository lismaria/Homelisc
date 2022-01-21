from django.shortcuts import render, redirect
from Vendor.models import Shop

# Create your views here.

def check_vendor_details(request,render_template,id):
    if not request.user.is_authenticated:
        return redirect("home")
    elif (request.user.is_authenticated and request.user.is_vendor == True):
        shopInfo = Shop.objects.filter(id=id)
        shopCount = shopInfo.count()
        if shopCount == 0:
            return render(request,'Vendor/perks.html')
        else:
            return render(request,"Vendor/"+render_template+".html",{'shopInfo':shopInfo}) #*
    else:
        return redirect("home")

def home(request):
    # context=[]
    if not request.user.is_authenticated:
        return render(request,'home.html',{'food':'chocolates'})
    elif (request.user.is_authenticated and request.user.is_vendor == True):
        shopInfo = Shop.objects.filter(shop_owner_id=request.user.id)
        shopCount = shopInfo.count()
        print(shopInfo)
        if shopCount == 0:
            return render(request,'Vendor/perks.html')
        else:
            return render(request,'Vendor/home.html',{'shopInfo':shopInfo})
    else:
        return render(request,'home.html',{'food':'chocolates'})

def register_shop(request):
    if not request.user.is_authenticated:
        return redirect("home")
    elif (request.user.is_authenticated and request.user.is_vendor == True):
        shopCount = Shop.objects.filter(shop_owner_id=request.user.id).count()
        if shopCount < 3:
            return render(request,'Vendor/register-shop.html')
        else:
            return redirect("home")
    else:
        return redirect("home")

def shop_view(request,id,slug):
    shopInfo = Shop.objects.filter(id=id)
    return render(request,"Vendor/shop.html",{'shopInfo':shopInfo})

def menu_view(request,id,slug):
    menu_view = check_vendor_details(request,"menu",id)
    return menu_view

def review_view(request,id,slug):
    reviews_view = check_vendor_details(request,"review",id)
    return reviews_view
