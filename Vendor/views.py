from django.shortcuts import render, redirect
from Vendor.models import Shop

# Create your views here.

def check_vendor_details(request,render_template):
    if not request.user.is_authenticated:
        return redirect("home")
    elif (request.user.is_authenticated and request.user.is_vendor == True):
        shopCount = Shop.objects.filter(shop_owner_id=request.user.id).count()
        if shopCount == 0:
            return render(request,'Vendor/perks.html')
        else:
            return render(request,"Vendor/"+render_template+".html") #*
    else:
        return redirect("home")

def shop_view(request):
    # context=[]
    if not request.user.is_authenticated:
        return render(request,'home.html',{'food':'chocolates'})
    elif (request.user.is_authenticated and request.user.is_vendor == True):
        shopCount = Shop.objects.filter(shop_owner_id=request.user.id).count()
        shopInfo = Shop.objects.filter(shop_owner_id=request.user.id)
        print(shopInfo)
        # context['shopInfo'] = shopInfo
        # for i in shopInfo:
        #     print("I",i.id)
        if shopCount == 0:
            return render(request,'Vendor/perks.html')
        else:
            return render(request,'Vendor/home.html',{'shopInfo':shopInfo})
    else:
        return render(request,'home.html',{'food':'chocolates'})

def menu_view(request):
    menu_view = check_vendor_details(request,"menu")
    return menu_view

def review_view(request):
    reviews_view = check_vendor_details(request,"review")
    return reviews_view

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

def shop(request,shop_idd):
    return render(request,"Vendor/shop.html")