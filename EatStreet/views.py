from http.client import GATEWAY_TIMEOUT
import math
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from Vendor.models import Category, ItemImage, Shop, Item, Review, VendorReply, Wishlist
from Vendor.forms import ReplyPostForm, ReviewForm
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

def home(request):
    pass

def wishlist_arrs(id):
    userwish = Wishlist.objects.filter(user_id=id)
    useritemwish = []
    usershopwish = []
    for i in userwish:
        if i.item_id == None:
            usershopwish.append(i.shop_id.id)
        else:
            useritemwish.append(i.item_id.id)
    return (usershopwish, useritemwish)

@csrf_exempt
def search(request):        
    if request.POST:
        print(request.POST['searchVal'])
    else:
        categories = Category.objects.all()
        # if 'term' in request.GET:
        #     print('term')
        #     shopqs = Shop.objects.filter(shop_name__icontains=request.GET.get('term'))

        #     result = list()
        #     for shop in shopqs:
        #         result.append(shop.shop_name)
        #     # titles = [product.title for product in qs]
        #     print(result)
        # return JsonResponse(res, safe=False)
        return render(request,"search.html",{'categories':categories})
    return render(request,"search.html")

def wishlist(request):
    shopWishlists = Wishlist.objects.filter(user_id_id=request.user.id,item_id_id__isnull=True)
    itemWishlists = Wishlist.objects.filter(user_id_id=request.user.id,item_id_id__isnull=False)
    wishlist_count = shopWishlists.count()+itemWishlists.count()
    return render(request,"wishlist.html",{"shopWishlists":shopWishlists,'itemWishlists':itemWishlists,'wishlist_count':wishlist_count})

def category(request):
    category = request.GET['c']
    categories = Category.objects.all()
    categoryInfo = {}
    try:
        categoryInfo = Category.objects.get(category_name=category)
    except Category.DoesNotExist:
        pass

    shopqs = Shop.objects.annotate(search=SearchVector('shop_name', 'shop_tags', 'shop_descr'),).filter(search=category)
    itemqs = Item.objects.annotate(search=SearchVector('item_name', 'item_category', 'item_descr',),).filter(search=category)

    usershopwish, useritemwish = wishlist_arrs(request.user.id)

    return render(request,"category.html",{'categoryInfo':categoryInfo,'categories':categories,'shopqs':shopqs,'itemqs':itemqs, 'usershopwish':usershopwish, 'useritemwish':useritemwish})

def product(request,id,slug,itemid):
    shopInfo = Shop.objects.filter(id=id)
    itemInfo = Item.objects.filter(id=itemid).order_by('-id')
    itemReviews = Review.objects.filter(item_id = itemid).order_by('-date')
    reviewForm = ReviewForm()
    vendorReplies = VendorReply.objects.filter(shop_id=id)

    usershopwish, useritemwish = wishlist_arrs(request.user.id)

    userlikes = Review.likes.through.objects.filter(user_id=request.user.id)
    userlikesarr=[]
    for i in userlikes:
        userlikesarr.append(i.review_id)

    obj = get_object_or_404(Shop, pk=id)
    if obj.shop_slug != slug:
        return redirect('shop', id=obj.pk, slug=obj.shop_slug, itemid=itemid)
    return render(request,"product.html",{'shopInfo':shopInfo,'itemInfo':itemInfo,'itemReviews':itemReviews,'reviewForm':reviewForm,'vendorReplies':vendorReplies,'useritemwish':useritemwish,'userlikesarr':userlikesarr})

def shop(request,id,slug):
    itemInfo = Item.objects.filter(shop_id=id).order_by('-id')
    shopInfo = Shop.objects.filter(id=id)
    obj = get_object_or_404(Shop, pk=id)

    usershopwish, useritemwish = wishlist_arrs(request.user.id)

    if obj.shop_slug != slug:
        return redirect('shop', id=obj.pk, slug=obj.shop_slug)
    return render(request,"shop.html",{'shopInfo':shopInfo,'itemInfo':itemInfo,'usershopwish':usershopwish, 'useritemwish':useritemwish})

def reviews(request,id,slug):
    shopInfo = Shop.objects.filter(id=id)
    shopReviews = Review.objects.filter(shop_id=id, item_id__isnull = True).order_by('-date')
    reviewForm = ReviewForm()
    vendorReplies = VendorReply.objects.filter(shop_id=id)

    usershopwish, useritemwish = wishlist_arrs(request.user.id)

    userlikes = Review.likes.through.objects.filter(user_id=request.user.id)
    userlikesarr=[]
    for i in userlikes:
        userlikesarr.append(i.review_id)

    obj = get_object_or_404(Shop, pk=id)
    if obj.shop_slug != slug:
        return redirect('reviews', id=obj.pk, slug=obj.shop_slug)
    return render(request,"reviews.html",{'shopInfo':shopInfo,'shopReviews':shopReviews,'reviewForm':reviewForm,'vendorReplies':vendorReplies,'userlikesarr':userlikesarr, 'usershopwish':usershopwish})

def review_post(request):
    if not request.user.is_authenticated:
        return render(request,"Account/account.html")
        
    if request.POST:
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
            stars = int(request.POST.get('stars'))
            print(stars)

            if request.POST.get('itemid'):
                item_oldreviews = Review.objects.filter(item_id = itemid)
                item_total_stars = item_oldreviews.aggregate(Sum('stars'))['stars__sum']
                item_reviewcount = item_oldreviews.count()
                if(itemInfo.item_rating == None):
                    itemInfo.item_rating = instance.stars/1
                else:
                    itemInfo.item_rating = round((item_total_stars + stars) / (item_reviewcount+1), 1) 
                itemInfo.save()
                instance.item_id = itemInfo

            else:
                shop_oldreviews = Review.objects.filter(shop_id=shopid, item_id__isnull=True)
                shop_total_stars = shop_oldreviews.aggregate(Sum('stars'))['stars__sum']
                shop_reviewcount = shop_oldreviews.count()
                if(shopInfo.shop_rating == None):
                    shopInfo.shop_rating = instance.stars/1
                else:
                    shopInfo.shop_rating = round((shop_total_stars + stars) / (shop_reviewcount+1), 1)
                shopInfo.save()

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
            data = Wishlist.objects.filter(user_id_id = request.user.id, shop_id_id = shopid, item_id_id = itemid)
        else:
            data = Wishlist.objects.filter(user_id_id = request.user.id, shop_id_id = shopid, item_id_id__isnull = True)
            print(data)
        
        if data.exists():
            data.delete()
            if request.POST.get('item_heartid'):
                print("found item")
                itemInfo = Item.objects.filter(id=itemid).values()
                count = itemInfo[0]['item_wishlist_count']
                count-=1
                Item.objects.filter(id=itemid).update(item_wishlist_count = count)
            else:
                print("found shop")
                shopInfo = Shop.objects.filter(id=shopid).values()
                count = shopInfo[0]['shop_wishlist_count']
                count-=1
                Shop.objects.filter(id=shopid).update(shop_wishlist_count = count)

            return JsonResponse({"msg": "Removed from wishlist"}, status=200)
        else:
            if request.POST.get('item_heartid'):
                print("not found item")
                Wishlist.objects.create(user_id_id = request.user.id,shop_id_id = shopid, item_id_id = itemid)
                itemInfo = Item.objects.filter(id=itemid).values()
                count = itemInfo[0]['item_wishlist_count']
                count+=1
                Item.objects.filter(id=itemid).update(item_wishlist_count = count)
            else:
                print("not found shop")
                Wishlist.objects.create(user_id_id = request.user.id,shop_id_id = shopid)
                shopInfo = Shop.objects.filter(id=shopid).values()
                count = shopInfo[0]['shop_wishlist_count']
                count+=1
                Shop.objects.filter(id=shopid).update(shop_wishlist_count = count)
            return JsonResponse({"msg": "Added to wishlist"}, status=200)

    else:
        return JsonResponse({"error": " "}, status=400)



@csrf_exempt
def review_like(request):
    if not request.user.is_authenticated:
        return render(request,"Account/account.html")
        
    if request.POST:
        reviewid = request.POST.get('reviewid')
        review = get_object_or_404(Review, id=reviewid)
        
        if review.likes.filter(id=request.user.id).exists():
            review.likes.remove(request.user)
        else:
            review.likes.add(request.user)
        likes = review.likes_count()
        return JsonResponse({"likes": likes}, status=200)

    else:
        return JsonResponse({"error": " "}, status=400)