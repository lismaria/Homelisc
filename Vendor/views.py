from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.core import serializers
from Vendor.models import Shop
from Account.models import User
from Vendor.forms import ShopCreationForm
from Account.forms import AccountUpdationForm

# Create your views here.

def check_vendor_details(request, render_template, id, slug):
    if not request.user.is_authenticated:
        return redirect("home")
    elif (request.user.is_authenticated and request.user.is_vendor == True):
        shop_owner = Shop.objects.values('shop_owner').get(id=id)['shop_owner']
        if(request.user.id == shop_owner):
            shopInfo = Shop.objects.filter(id=id)
            obj = get_object_or_404(Shop, pk=id)
            print(obj)
            if obj.shop_slug != slug:
                print("O: ",obj.shop_slug, "S: ",slug)
                return redirect('vendor:'+render_template, id=obj.pk, slug=obj.shop_slug)
            return render(request,"Vendor/"+render_template+".html",{'shopInfo':shopInfo})
        else:
            return redirect("home")
    else:
        return redirect("home")

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
            return render(request,'Vendor/home.html',{'shopInfo':shopInfo,'vendorForm':vendorForm})
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

def shop_view(request,id,slug):
    shop_view = check_vendor_details(request,"shop",id, slug)
    return shop_view

def menu_view(request,id,slug):
    menu_view = check_vendor_details(request,"menu",id, slug)
    return menu_view

def review_view(request,id,slug):
    reviews_view = check_vendor_details(request,"review",id, slug)
    return reviews_view

def vendor_update(request):
    print("In verdor_update")
    if not request.user.is_authenticated:
        return render(request,"Account/account.html")
        
    # context = {}
    if request.POST:
        print("In req.ajax")
        # email = request.user.email
        form = AccountUpdationForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            print("Valid form")
            instance = form.save()
            # serialize in new friend object in json
            ser_instance = serializers.serialize('json', [ instance, ])
            return JsonResponse({"instance": ser_instance}, status=200)
            # return redirect("account:account")
        else:
            print("Invalid form")
            # user = User.objects.get(email=email)
            return JsonResponse({"error": form.errors}, status=400)
            # print(user)
    # else:
    #     user = User.objects.get(email=request.user.email)
    #     form = AccountUpdationForm(initial={'name':request.user.name,'email':request.user.email})
        
    # context['user'] = user
    # context['form'] = form
    # return render(request,"Account/account.html",context)
    print("Direct last")
    return JsonResponse({"error": ""}, status=400)

"""    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "POST":
        # get the form data
        form = FriendForm(request.POST)  # AccountUpdationForm(request.POST, request.FILES, instance=request.user)
        # save the data and after fetch the object in instance
        if form.is_valid():
            instance = form.save()
            # serialize in new friend object in json
            ser_instance = serializers.serialize('json', [ instance, ])
            # send to client side.
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            # some form errors occured.
            return JsonResponse({"error": form.errors}, status=400)

    # some error occured
    return JsonResponse({"error": ""}, status=400) """