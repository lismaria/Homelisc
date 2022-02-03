from http.client import GATEWAY_TIMEOUT
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from Vendor.models import Shop, Item, Review, VendorReply, Wishlist
from Vendor.forms import ReplyPostForm, ReviewForm
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

def home(request):
    pass

@csrf_exempt
def search(request):        
    if request.POST:
        print("Post")
        print(request.POST['searchVal'])
    else:
        print("search")
        shopNames = Shop.objects.all()
        itemNames = Item.objects.all()
        # if 'term' in request.GET:
        #     print('term')
        #     shopqs = Shop.objects.filter(shop_name__icontains=request.GET.get('term'))

        #     result = list()
        #     for shop in shopqs:
        #         result.append(shop.shop_name)
        #     # titles = [product.title for product in qs]
        #     print(result)
        # return JsonResponse(res, safe=False)
        return render(request,"search.html",{'shopNames':shopNames, 'itemNames': itemNames})
    return render(request,"search.html")

def wishlist(request):
    shopWishlists = Wishlist.objects.filter(user_id_id=request.user.id,item_id_id__isnull=True)
    itemWishlists = Wishlist.objects.filter(user_id_id=request.user.id,item_id_id__isnull=False)
    wishlist_count = shopWishlists.count()+itemWishlists.count()
    return render(request,"wishlist.html",{"shopWishlists":shopWishlists,'itemWishlists':itemWishlists,'wishlist_count':wishlist_count})

def category(request):
    category = request.GET['category']
    return render(request,"category.html",{'category':category})

def product(request,id,slug,itemid):
    shopInfo = Shop.objects.filter(id=id)
    itemInfo = Item.objects.filter(id=itemid).order_by('-id')
    itemReviews = Review.objects.filter(item_id = itemid).order_by('-date')
    reviewForm = ReviewForm()
    vendorReplies = VendorReply.objects.filter(shop_id=id)

    obj = get_object_or_404(Shop, pk=id)
    if obj.shop_slug != slug:
        return redirect('shop', id=obj.pk, slug=obj.shop_slug, itemid=itemid)
    return render(request,"product.html",{'shopInfo':shopInfo,'itemInfo':itemInfo,'itemReviews':itemReviews,'reviewForm':reviewForm,'vendorReplies':vendorReplies})

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
    vendorReplies = VendorReply.objects.filter(shop_id=id)
    for i in shopReviews:
        print(i.heart_by_owner)

    obj = get_object_or_404(Shop, pk=id)
    if obj.shop_slug != slug:
        return redirect('reviews', id=obj.pk, slug=obj.shop_slug)
    return render(request,"reviews.html",{'shopInfo':shopInfo,'shopReviews':shopReviews,'reviewForm':reviewForm,'vendorReplies':vendorReplies})

def review_post(request):
    if not request.user.is_authenticated:
        return render(request,"Account/account.html")
        
    if request.POST:
        print(request.POST)
        print(request.FILES)
        shopid = request.POST['shopid']
        shopInfo = Shop.objects.get(id=shopid)
        if request.POST.get('itemid'):
            itemid = request.POST.get('itemid')
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

@csrf_exempt
def add_wishlist(request):
    if not request.user.is_authenticated:
        return redirect(request,"Account/account.html")

    if request.POST:
        shopid = request.POST['shop_heartid']
        if request.POST.get('item_heartid'):
            itemid = request.POST.get('item_heartid')
            data = Wishlist.objects.filter(user_id_id = request.user.id,shop_id_id = shopid, item_id_id = itemid)
        else:
            data = Wishlist.objects.filter(user_id_id = request.user.id,shop_id_id = shopid)
        
        if data.exists():
            data.delete()
            if request.POST.get('item_heartid'):
                itemInfo = Item.objects.filter(id=itemid).values()
                count = itemInfo[0]['item_wishlist_count']
                count-=1
                Item.objects.filter(id=itemid).update(item_wishlist_count = count)
            else:
                shopInfo = Shop.objects.filter(id=shopid).values()
                count = shopInfo[0]['shop_wishlist_count']
                count-=1
                Shop.objects.filter(id=shopid).update(shop_wishlist_count = count)

            return JsonResponse({"msg": "Removed from wishlist"}, status=200)
        else:
            if request.POST.get('item_heartid'):
                Wishlist.objects.create(user_id_id = request.user.id,shop_id_id = shopid, item_id_id = itemid)
                itemInfo = Item.objects.filter(id=itemid).values()
                count = itemInfo[0]['item_wishlist_count']
                count+=1
                Item.objects.filter(id=itemid).update(item_wishlist_count = count)
            else:
                Wishlist.objects.create(user_id_id = request.user.id,shop_id_id = shopid)
                shopInfo = Shop.objects.filter(id=shopid).values()
                count = shopInfo[0]['shop_wishlist_count']
                count+=1
                Shop.objects.filter(id=shopid).update(shop_wishlist_count = count)
            return JsonResponse({"msg": "Added to wishlist"}, status=200)

    else:
        return JsonResponse({"error": " "}, status=400)