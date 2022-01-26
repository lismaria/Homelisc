from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core import serializers
from Vendor.models import Shop
from Account.models import User
from Vendor.forms import ShopCreationForm
from Account.forms import AccountUpdationForm

# Create your views here.

def check_vendor_details(request, id):
    if not request.user.is_authenticated:
        return None
    elif (request.user.is_authenticated and request.user.is_vendor == True):
        vendorForm = AccountUpdationForm(initial={'name':request.user.name,'email':request.user.email})
        shop_owner = Shop.objects.values('shop_owner').get(id=id)['shop_owner']
        if(request.user.id == shop_owner):
            shopInfo = Shop.objects.filter(id=id)
            return ({'shopInfo':shopInfo,'vendorForm':vendorForm})
        else:
            return None
    else:
        return None



def home(request):
    # context=[]
    if not request.user.is_authenticated:
        return render(request,'home.html',{'food':'chocolates'})
    elif (request.user.is_authenticated and request.user.is_vendor == True):
        vendorForm = AccountUpdationForm(initial={'name':request.user.name,'email':request.user.email})
        shopInfo = Shop.objects.filter(shop_owner_id=request.user.id)
        shopCount = shopInfo.count()
        if shopCount == 0:
            return render(request,'Vendor/perks.html')
        else:
            return render(request,'Vendor/home.html',{'shopInfo':shopInfo,'shopCount':shopCount,'vendorForm':vendorForm})
    else:
        return render(request,'home.html',{'food':'chocolates'})



def register_shop(request):
    if not request.user.is_authenticated:
        return redirect("home")
    
    context={}
    if request.method == 'POST':
        form = ShopCreationForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.shop_owner_id = request.user.id
            instance.save()
            return redirect("home")

    elif(request.user.is_vendor == True):
        shopCount = Shop.objects.filter(shop_owner_id=request.user.id).count()
        if shopCount < 3:
            form = ShopCreationForm()
            context['form'] = form
            return render(request,'Vendor/register-shop.html',context)
        else:
            return redirect("home")
            
    else:
        return redirect("home")

    context['form'] = form
    return render(request,'Vendor/register-shop.html',context)



def shop_view(request,id, slug):
    shopobj = check_vendor_details(request,id)
    if shopobj==None:
        return redirect("home")
    shopInfo = shopobj['shopInfo'].values()
    vendorForm = shopobj['vendorForm']
    shopForm = ShopCreationForm(initial={'shop_name':shopInfo[0]['shop_name'],'shop_tags':shopInfo[0]['shop_tags'],'shop_descr':shopInfo[0]['shop_descr'],'shop_contact':shopInfo[0]['shop_contact'],'shop_state':shopInfo[0]['shop_state'],'shop_city':shopInfo[0]['shop_city'],'shop_location':shopInfo[0]['shop_location'],'shop_logo':shopInfo[0]['shop_logo']})
    obj = get_object_or_404(Shop, pk=id)
    if obj.shop_slug != slug:
        return redirect('vendor:shop', id=obj.pk, slug=obj.shop_slug)
    return render(request,"Vendor/shop.html",{'shopInfo':shopInfo,'vendorForm':vendorForm,'shopForm':shopForm})



def menu_view(request,id,slug):
    shopobj = check_vendor_details(request,id)
    if shopobj==None:
        return redirect("home")
    obj = get_object_or_404(Shop, pk=id)
    if obj.shop_slug != slug:
        return redirect('vendor:shop', id=obj.pk, slug=obj.shop_slug)
    return render(request,"Vendor/menu.html",{'shopInfo':shopobj['shopInfo'],'vendorForm':shopobj['vendorForm']})



def review_view(request,id,slug):
    shopobj = check_vendor_details(request,id)
    if shopobj==None:
        return redirect("home")
    obj = get_object_or_404(Shop, pk=id)
    if obj.shop_slug != slug:
        return redirect('vendor:shop', id=obj.pk, slug=obj.shop_slug)
    return render(request,"Vendor/review.html",{'shopInfo':shopobj['shopInfo'],'vendorForm':shopobj['vendorForm']})



def vendor_update(request):
    if not request.user.is_authenticated:
        return render(request,"Account/account.html")
        
    if request.POST:
        print(request.FILES)
        form = AccountUpdationForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            instance = form.save()
            request.user.save()
            # serialize in new friend object in json
            ser_instance = serializers.serialize('json', [ instance, ])
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            return JsonResponse({"error": form.errors}, status=400)

    return JsonResponse({"error": ""}, status=400)



def shop_update(request):
    if not request.user.is_authenticated:
        return render(request,"Account/account.html")
        
    if request.POST:
        print("post req")
        shopInfo = Shop.objects.get(id=12)
        print(shopInfo)
        print(request.POST)
        print(request.FILES)
        form = ShopCreationForm(request.POST, request.FILES, instance=shopInfo)
        if form.is_valid():
            print("valid form")
            instance = form.save()
            # serialize in new friend object in json
            ser_instance = serializers.serialize('json', [ instance, ])
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            print("not valid")
            return JsonResponse({"error": form.errors}, status=400)

    return JsonResponse({"error": ""}, status=400)