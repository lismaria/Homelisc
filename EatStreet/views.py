from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from Vendor.models import Shop, ShopReview, Item, ItemReview

def home(request):
    print("in home")
    shops = Shop.objects.all()
    print(shops.count())
    return render(request,'home.html',{'food':'chocolates'})

def search(request):
    return render(request,"search.html")

def wishlist(request):
    return render(request,"wishlist.html")

def category(request):
    category = request.GET['category']
    return render(request,"category.html",{'category':category})

def product(request,id,slug,itemid):
    shopInfo = Shop.objects.filter(id=id)
    itemInfo = Item.objects.filter(id=itemid).order_by('-id')
    itemReviews = ItemReview.objects.filter(item_id = itemid).order_by('-date')
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
    shopReviews = ShopReview.objects.filter(shop_id=id).order_by('-date')
    obj = get_object_or_404(Shop, pk=id)
    if obj.shop_slug != slug:
        return redirect('reviews', id=obj.pk, slug=obj.shop_slug)
    return render(request,"reviews.html",{'shopInfo':shopInfo,'shopReviews':shopReviews})
