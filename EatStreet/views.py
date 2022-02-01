from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from Vendor.models import Shop, Item, Review
from Vendor.forms import ReplyPostForm, ReviewForm
from django.core import serializers

def home(request):
    print("in home")
    shops = Shop.objects.all()
    print(shops.count())
    return render(request,'home.html',{'food':'chocolates'})

def search(request):
    print("search")
    if 'term' in request.GET:
        print('term')
        shopqs = Shop.objects.filter(shop_name__icontains=request.GET.get('term'))
        result = list()
        for shop in shopqs:
            result.append(shop.shop_name)
        # titles = [product.title for product in qs]
        print(result)
        return JsonResponse(result, safe=False)
    return render(request,"search.html")

def wishlist(request):
    return render(request,"wishlist.html")

def category(request):
    category = request.GET['category']
    return render(request,"category.html",{'category':category})

def product(request,id,slug,itemid):
    shopInfo = Shop.objects.filter(id=id)
    itemInfo = Item.objects.filter(id=itemid).order_by('-id')
    itemReviews = Review.objects.filter(item_id = itemid).order_by('-date')

    obj = get_object_or_404(Shop, pk=id)
    if obj.shop_slug != slug:
        return redirect('shop', id=obj.pk, slug=obj.shop_slug, itemid=itemid)
    return render(request,"product.html",{'shopInfo':shopInfo,'itemInfo':itemInfo,'itemReviews':itemReviews})

def shop(request,id,slug):
    itemInfo = Item.objects.filter(shop_id=id).order_by('-id')
    shopInfo = Shop.objects.filter(id=id)
    obj = get_object_or_404(Shop, pk=id)
    if obj.shop_slug != slug:
        return redirect('shop', id=obj.pk, slug=obj.shop_slug)
    return render(request,"shop.html",{'shopInfo':shopInfo,'itemInfo':itemInfo})

def reviews(request,id,slug):
    shopInfo = Shop.objects.filter(id=id)
    shopReviews = Review.objects.filter(shop_id=id, item_id__isnull = True).order_by('-date')
    reviewForm = ReviewForm()
    obj = get_object_or_404(Shop, pk=id)
    if obj.shop_slug != slug:
        return redirect('reviews', id=obj.pk, slug=obj.shop_slug)
    return render(request,"reviews.html",{'shopInfo':shopInfo,'shopReviews':shopReviews,'reviewForm':reviewForm})

def review_post(request):
    if not request.user.is_authenticated:
        return render(request,"Account/account.html")
        
    if request.POST:
        print(request.POST)
        print(request.FILES)
        shopid = request.POST['shopid']
        print("s: ",shopid)
        shopInfo = Shop.objects.get(id=shopid)
        if request.POST.get('itemid'):
            itemid = request.POST.get('itemid')
            print("i: ",itemid)
            itemInfo = Item.objects.get(id=itemid)
        
        reviewForm = ReviewForm(request.POST,request.FILES)
        if reviewForm.is_valid():
            instance = reviewForm.save(commit=False)
            instance.user_id = request.user
            instance.shop_id = shopInfo
            if request.POST.get('itemid'):
                instance.item_id = itemInfo
            instance.save()
            ser_instance = serializers.serialize('json', [ instance, ])
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            return JsonResponse({"error": reviewForm.errors}, status=400)
    return JsonResponse({"error": " "}, status=400)