from django.shortcuts import render, redirect
from Vendor.models import Shop

# Create your views here.

def vendor_view(request):
    if not request.user.is_authenticated:
        return render(request,'home.html',{'food':'chocolates'})
    elif (request.user.is_authenticated and request.user.is_vendor == True):
        shopCount = Shop.objects.filter(shop_owner_id=request.user.id).count()
        if shopCount == 0:
            return render(request,'Vendor/perks.html')
        else:
            return render(request,'Vendor/vendor.html')
    else:
        return redirect("home")

def review_view(request):
    if not request.user.is_authenticated:
        return redirect("home")
    elif (request.user.is_authenticated and request.user.is_vendor == True):
        shopCount = Shop.objects.filter(shop_owner_id=request.user.id).count()
        print(shopCount)
        if shopCount == 0:
            return render(request,'Vendor/perks.html')
        else:
            return render(request,"Vendor/review.html") #*
    else:
        return redirect("home")
 