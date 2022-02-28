from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F, Sum, Count
from django.db.models.functions import TruncDate
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core import serializers
import numpy as np
from Vendor.models import Category, Item, Review, Shop, ItemImage, VendorReply, Wishlist, Theme
from Vendor.forms import ReplyPostForm, ShopCreationForm, ItemCreationForm, ItemImageUploadForm, ItemImageEditForm
from Account.forms import AccountUpdationForm
import pandas as pd
import datetime
import math
import random


# IND = pytz.timezone('Asia/Kolkata')
# from django.utils import timezone
# import zoneinfo
# ind = zoneinfo.ZoneInfo('Asia/Calcutta')

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



def getThemeOfTheDay(categories):
    theme = Theme.objects.filter(date=datetime.datetime.now().strftime('%Y-%m-%d')).values()
    if theme:
        theme_items = Item.objects.filter(item_category__contains=[theme[0]['theme']]).order_by(F('item_rating').desc(nulls_last=True),'-item_clicks_count','-item_wishlist_count')[:4]
        themeotd = theme[0]['theme']
    else:
        catlist = [i.category_name for i in categories]
        created_theme = Theme.objects.create(theme=random.choice(catlist),date=datetime.datetime.now().strftime('%Y-%m-%d'))
        theme_items = Item.objects.filter(item_category__contains=[created_theme]).order_by(F('item_rating').desc(nulls_last=True),'-item_clicks_count','-item_wishlist_count')[:4]
        themeotd = created_theme
    return theme_items, themeotd



def home(request):

    if not request.user.is_authenticated:
        categories = Category.objects.all()
        theme_items, themeotd = getThemeOfTheDay(categories)

        shops = Shop.objects.order_by(F('shop_rating').desc(nulls_last=True),'-shop_clicks_count','-shop_wishlist_count')[:6]
        topcats = Category.objects.order_by('-category_count')[:10]
        bestpicks = Item.objects.order_by(F('item_rating').desc(nulls_last=True),'-item_clicks_count','-item_wishlist_count')[:4]
        return render(request,'home.html',{'shops':shops,'categories':categories, 'topcats':topcats, 'bestpicks':bestpicks,'themeotd':themeotd,'theme_items':theme_items})

    elif (request.user.is_authenticated and request.user.is_vendor == True):
        vendorForm = AccountUpdationForm(initial={'name':request.user.name,'email':request.user.email})
        shopInfo = Shop.objects.filter(shop_owner_id=request.user.id).order_by('-id')
        shopCount = shopInfo.count()
        
        if shopCount == 0:
            return render(request,'Vendor/perks.html')
        else:
            return render(request,'Vendor/home.html',{'shopInfo':shopInfo,'shopCount':shopCount,'vendorForm':vendorForm})
    
    else:
        categories = Category.objects.all()
        theme_items, themeotd = getThemeOfTheDay(categories)

        shops = Shop.objects.order_by(F('shop_rating').desc(nulls_last=True),F('shop_wishlist_count').desc(nulls_last=True))[:6]
        topcats = Category.objects.order_by('-category_count')[:10]
        userwish = Wishlist.objects.filter(user_id=request.user.id)
        bestpicks = Item.objects.order_by(F('item_rating').desc(nulls_last=True),F('item_wishlist_count').desc(nulls_last=True))[:4]
        useritemwish = []
        usershopwish = []
        for i in userwish:
            if i.item_id == None:
                usershopwish.append(i.shop_id.id)
            else:
                useritemwish.append(i.item_id.id)
        return render(request,'home.html',{'shops':shops,'categories':categories, 'topcats':topcats, 'usershopwish':usershopwish, 'useritemwish':useritemwish, 'bestpicks':bestpicks,'themeotd':themeotd,'theme_items':theme_items})



def register_shop(request):
    if not request.user.is_authenticated:
        return redirect("home")
    
    context={}
    if request.method == 'POST':
        shopcat = request.POST.get('shop_tags')
        shopcatarr = shopcat.split(',')
        form = ShopCreationForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.shop_owner_id = request.user.id
            instance.save()

            for i in shopcatarr:
                cat = Category.objects.filter(category_name=i.lower().strip())
                if(cat):
                    count = cat.values()[0]['category_count']
                    count += 1
                    Category.objects.filter(category_name=i.lower().strip()).update(category_count = count )
                else:
                    Category.objects.create(category_name = i.lower().strip())
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



def shop_view(request, id, slug):
    shopobj = check_vendor_details(request,id)
    if shopobj==None:
        return redirect("home")
    shopInfo = shopobj['shopInfo']
    vendorForm = shopobj['vendorForm']
    shop_details = shopobj['shopInfo'].values()

    shopForm = ShopCreationForm(initial={'shop_name':shop_details[0]['shop_name'],'shop_tags':shop_details[0]['shop_tags'],'shop_descr':shop_details[0]['shop_descr'],'shop_contact':shop_details[0]['shop_contact'],'shop_state':shop_details[0]['shop_state'],'shop_city':shop_details[0]['shop_city'],'shop_location':shop_details[0]['shop_location'],'shop_logo':shop_details[0]['shop_logo']})
    obj = get_object_or_404(Shop, pk=id)
    if obj.shop_slug != slug:
        return redirect('vendor:shop', id=obj.pk, slug=obj.shop_slug)
    return render(request,"Vendor/shop.html",{'shopInfo':shopInfo,'vendorForm':vendorForm,'shopForm':shopForm})



def shop_insights(request):
    context = {}
    shopid = request.GET['shopid']

    # Shop Rating by day (past week) Area Chart
    revpday = Review.objects.filter(shop_id=shopid).annotate(day=TruncDate('date')).values('day').annotate(Count('stars'),Sum('stars')).order_by('day')
    rdf = pd.DataFrame(revpday)

    if not rdf.empty:
        today = datetime.date.today()

        until = 6
        date_list = []
        rating_list = []
        for i in range(until,-1,-1):
            delta = datetime.timedelta(days=i)
            until_date = today - delta
            date_list.append(until_date.strftime("%d %b, %Y"))      

            rdfview= rdf[(rdf['day'] <= until_date)]
            until_avg = np.sum(rdfview['stars__sum'])/np.sum(rdfview['stars__count'])
            rating_list.append(round(until_avg,1))
        rating_list = [0 if math.isnan(x) else x for x in rating_list]
        context['date_list'] = date_list
        context['rating_list'] = rating_list
        context['shoplinechart'] = True
    else:
        context['shoplinechart'] = False


    # Shop rating pie chart 
    shopRating = Review.objects.filter(shop_id=shopid).values('stars').annotate(Count('stars')).order_by('-stars')
    if shopRating:
        shopRdf = pd.DataFrame(shopRating)
        
        init_list = [{'stars':1,'stars__count':0},{'stars':2,'stars__count':0},{'stars':3,'stars__count':0},{'stars':4,'stars__count':0},{'stars':5,'stars__count':0}]
        init_df = pd.DataFrame(init_list)
        init_df.set_index('stars',inplace=True)
        shopRdf.set_index('stars',inplace=True)
        missing_index = init_df.index.difference(shopRdf.index)

        final_df = pd.concat([shopRdf,init_df.loc[missing_index, :]])
        final_df.reset_index(drop=False,inplace=True)
        final_df.sort_values('stars',ascending=False,inplace=True)
        context['shopRatingPie'] = final_df['stars__count'].to_list()
        context['shopratingpie'] = True
    else:
        context['shopratingpie'] = False


    # Item Wihslist/Visit Count
    itemwishclick = Item.objects.filter(shop_id=shopid).values_list('item_name','item_wishlist_count','item_clicks_count').order_by('item_name')
    if itemwishclick:
        wishclick_item_name = []
        item_wish_count = []
        item_click_count = []
        for i in itemwishclick:
            wishclick_item_name.append(i[0])
            item_wish_count.append(i[1])
            item_click_count.append(i[2])

        context['wishclick_item_name'] = wishclick_item_name
        context['item_wish_count'] = item_wish_count
        context['item_click_count'] = item_click_count
        context['itemwishclick'] = True
    else:
        context['itemwishclick'] = False

    # Item rating bar Chart
    itemrough = Review.objects.filter(shop_id=shopid, item_id__isnull=False).values("item_id__item_name","stars").annotate(Count('stars')).order_by('item_id__item_name')
    df = pd.DataFrame(itemrough)
    if not df.empty:
        df = df.pivot_table('stars__count','item_id__item_name','stars')
        cols = [1,2,3,4,5]
        df2 = df.reindex(df.columns.union(cols, sort=None), axis=1, fill_value=0)
        df2.fillna(0,inplace=True)
        df2.reset_index(drop=False,inplace=True)

        item_name = df2['item_id__item_name'].to_list()
        item_stars_count_5 = df2.iloc[:,5].to_list()
        item_stars_count_4 = df2.iloc[:,4].to_list()
        item_stars_count_3 = df2.iloc[:,3].to_list()
        item_stars_count_2 = df2.iloc[:,2].to_list()
        item_stars_count_1 = df2.iloc[:,1].to_list()

        context['item_name'] = item_name
        context['item_stars_count_5'] = item_stars_count_5
        context['item_stars_count_4'] = item_stars_count_4
        context['item_stars_count_3'] = item_stars_count_3
        context['item_stars_count_2'] = item_stars_count_2
        context['item_stars_count_1'] = item_stars_count_1
        context['itemratingstack'] = True
    else:
        context['itemratingstack'] = False

    return render(request, "Vendor/insights.html", context)
    # return render(request, "Vendor/insights.html", {'shopRatingPie': shopRatingPie,'wishclick_item_name':wishclick_item_name,'item_wish_count':item_wish_count,'item_click_count':item_click_count,'item_name':item_name,'item_stars_count_5':item_stars_count_5,'item_stars_count_4':item_stars_count_4,'item_stars_count_3':item_stars_count_3,'item_stars_count_2':item_stars_count_2,'item_stars_count_1':item_stars_count_1,'date_list':date_list,'rating_list':rating_list})



def menu_view(request,id,slug):
    shopobj = check_vendor_details(request,id)
    itemInfo = Item.objects.filter(shop_id=id).order_by('-id')
    # imageInfo = ItemImage.objects.filter(shop_id=id).distinct('item_id')
    itemForm = ItemCreationForm()
    imageForm = ItemImageUploadForm()
    itemcount = itemInfo.count()
    if shopobj==None:
        return redirect("home")
    obj = get_object_or_404(Shop, pk=id)
    if obj.shop_slug != slug:
        return redirect('vendor:shop', id=obj.pk, slug=obj.shop_slug)
    return render(request,"Vendor/menu.html",{'shopInfo':shopobj['shopInfo'],'vendorForm':shopobj['vendorForm'],'itemForm':itemForm, 'imageForm':imageForm, 'itemInfo':itemInfo,'itemcount':itemcount})



def review_view(request,id,slug):
    shopobj = check_vendor_details(request,id)
    if shopobj==None:
        return redirect("home")
    reviews = Review.objects.filter(shop_id=id).order_by('-date')
    items = Review.objects.filter(shop_id=id,item_id__isnull=False).distinct('item_id')
    vendorReplies = VendorReply.objects.filter(shop_id=id)
    replyForm = ReplyPostForm()
    obj = get_object_or_404(Shop, pk=id)
    if obj.shop_slug != slug:
        return redirect('vendor:shop', id=obj.pk, slug=obj.shop_slug)
    return render(request,"Vendor/review.html",{'shopInfo':shopobj['shopInfo'],'vendorForm':shopobj['vendorForm'],'reviews':reviews,'replyForm':replyForm,'vendorReplies':vendorReplies,'items':items})



def vendor_update(request):
    if not request.user.is_authenticated:
        return render(request,"Account/account.html")
        
    if request.POST:
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
        shopid = request.POST['shopid']
        shopcat = request.POST.get('shop_tags')
        shopcatarr = shopcat.split(',')
        shopInfo = Shop.objects.get(id=shopid)
        old_tags = shopInfo.shop_tags

        form = ShopCreationForm(request.POST, request.FILES, instance=shopInfo)
        if form.is_valid():
            instance = form.save()

            for i in shopcatarr:
                if i not in old_tags:
                    cat = Category.objects.filter(category_name=i.lower().strip())
                    if(cat):
                        count = cat.values()[0]['category_count']
                        count += 1
                        Category.objects.filter(category_name=i.lower().strip()).update(category_count = count )
                    else:
                        Category.objects.create(category_name = i.lower().strip())
            # serialize in new friend object in json
            ser_instance = serializers.serialize('json', [ instance, ])
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            return JsonResponse({"error": form.errors}, status=400)

    return JsonResponse({"error": ""}, status=400)



def item_add(request):
    if not request.user.is_authenticated:
        return render(request,"Account/account.html")
        
    if request.POST:        
        shopid = request.POST['shopid']
        itemcat = request.POST.get('item_category')
        itemcatarr = itemcat.split(',')
        shopInfo = Shop.objects.get(id=shopid)
        
        files = request.FILES.getlist('item_img')
        if files:
            itemForm = ItemCreationForm(request.POST)
            if itemForm.is_valid():
                instance = itemForm.save(commit=False)
                instance.shop_id = shopInfo
                instance.save()
                ser_instance = serializers.serialize('json', [ instance, ])

                for i in itemcatarr:
                    cat = Category.objects.filter(category_name=i.lower().strip())
                    if(cat):
                        count = cat.values()[0]['category_count']
                        count += 1
                        Category.objects.filter(category_name=i.lower().strip()).update(category_count = count )
                    else:
                        Category.objects.create(category_name = i.lower().strip())

            else:
                return JsonResponse({"error": itemForm.errors}, status=400)

            itemInfo = instance
            imageForm = ItemImageUploadForm(request.FILES)

            if imageForm.is_valid():
                ser_img=""
                for f in files:
                    # TRY 1
                    # instance = imageForm.save(commit=False)
                    # instance.shop_id = shopInfo
                    # instance.item_id = itemInfo
                    # print(f)
                    # instance.item_img = f
                    # instance.save()

                    # TRY 2
                    # image = form['image']
                    img = ItemImage(item_id=itemInfo, shop_id=shopInfo, item_img=f)
                    img.save()
                    ser_img = ser_img + serializers.serialize('json', [ img, ])
                    # return JsonResponse({"instance": ser_instance}, status=200)
                
                imageQuerySet = ItemImage.objects.filter(item_id=instance.id).distinct('item_id')
                for i in imageQuerySet:
                    instance.item_img_def = i.item_img
                instance.save()
            else:
                return JsonResponse({"error": imageForm.errors}, status=400)
        else:
            return JsonResponse({"noImgError": "Please attach atleast 1 image"}, status=400)
            
        return JsonResponse({"instance": ser_instance,"img_instance": ser_img }, status=200)
    return JsonResponse({"error": " "}, status=400)



def item_edit(request):
    if not request.user.is_authenticated:
        return render(request,"Account/account.html")  

    if request.POST:
        itemid = request.POST['itemid']
        itemcat = request.POST.get('item_category')
        itemcatarr = itemcat.split(',')
        itemInfo = Item.objects.get(id=itemid)
        old_tags = itemInfo.item_category

        itemForm = ItemCreationForm(request.POST, instance=itemInfo)
        if itemForm.is_valid():
            instance = itemForm.save()

            for i in itemcatarr:
                if i not in old_tags:
                    cat = Category.objects.filter(category_name=i.lower().strip())
                    if(cat):
                        count = cat.values()[0]['category_count']
                        count += 1
                        Category.objects.filter(category_name=i.lower().strip()).update(category_count = count )
                    else:
                        Category.objects.create(category_name = i.lower().strip())

            ser_instance = serializers.serialize('json', [ instance, ])
        else:
            return JsonResponse({"error": itemForm.errors}, status=400)

        imageForm = ItemImageUploadForm(request.FILES)
        files = request.FILES.getlist('item_img')
        shopid = request.POST['shopid']
        shopInfo = Shop.objects.get(id=shopid)
        imageQuerySet = ItemImage.objects.filter(item_id=itemid)
        imageInfo = imageQuerySet.values()
        imgcount = imageInfo.count()
        if imgcount <= 3:
            if imageForm.is_valid():
                ser_img=""
                for f in files:
                    img = ItemImage(item_id=itemInfo, shop_id=shopInfo, item_img=f)
                    img.save()
                    ser_img = ser_img + serializers.serialize('json', [ img, ])
                imageQuerySet = ItemImage.objects.filter(item_id=itemid).distinct('item_id')
                for i in imageQuerySet:
                    itemInfo.item_img_def = i.item_img
                itemInfo.save()
            else:
                return JsonResponse({"error": imageForm.errors}, status=400)
        else:
            return JsonResponse({"only3imgerr": "Only 3 images can be uploaded."}, status=400)
        return JsonResponse({"instance": ser_instance,"img_instance": ser_img }, status=200)
            
    else:
        # GET request
        itemid=request.GET.get('id')
        shopid=request.GET.get('shopid')
        itemInfo = Item.objects.filter(id=itemid).values()
        imageQuerySet = ItemImage.objects.filter(item_id=itemid)
        imageInfo = imageQuerySet.values()
        imgcount = imageInfo.count()
        filledImageForm = []
        count = []
        
        filledItemForm = ItemCreationForm(initial={'item_name':itemInfo[0]['item_name'],'item_descr':itemInfo[0]['item_descr'],'item_price':itemInfo[0]['item_price'],'item_category':itemInfo[0]['item_category']})
        imageForm = ItemImageEditForm()
        for i in range(0,imgcount):
            count.append(i)
            filledImageForm.append(ItemImageEditForm(initial={'item_img':imageInfo[i]['item_img']}))
        imageCombo = zip(filledImageForm, imageQuerySet, count)
        
        return render(request, 'Vendor/itemedit.html',{'itemid':itemid,'shopid':shopid,'imageForm':imageForm,'filledItemForm':filledItemForm, 'imageCombo':imageCombo})
    return JsonResponse({"error": " ", }, status=400)

@csrf_exempt
def itemimg_delete(request):
    print(request.FILES)
    if not request.user.is_authenticated:
        return render(request,"Account/account.html")
    
    if request.POST:
        deleteimgid = request.POST.get('deleteimgid')
        try:
            imageInfo = ItemImage.objects.filter(id=deleteimgid)
            if imageInfo:
                imageInfo.delete()
            else:
                raise Exception
        except:
            return JsonResponse({"error": "Failed to delete"}, status=400)
        else:
            return JsonResponse({"msg": "Image Deleted :("}, status=200)

    return JsonResponse({"error": " "}, status=400)



@csrf_exempt
def item_delete(request):
    if not request.user.is_authenticated:
        return render(request,"Account/account.html")
    
    if request.POST:
        remid = request.POST.get('remid')
        try:
            itemInfo = Item.objects.filter(id=remid)
            if itemInfo:
                itemInfo.delete()
            else:
                raise Exception
        except:
            return JsonResponse({"error": "Failed to delete"}, status=400)
        else:
            return JsonResponse({"msg": "Item Deleted :("}, status=200)

    return JsonResponse({"error": " "}, status=400)



def vendor_reply(request):
    if not request.user.is_authenticated:
        return render(request,"Account/account.html")
        
    if request.POST:
        shopid = request.POST['shop_id']
        reviewid = request.POST['review_id']

        shopInfo = Shop.objects.get(id=shopid)
        reviewInfo = Review.objects.get(id=reviewid)

        replyForm = ReplyPostForm(request.POST)
        if replyForm.is_valid():
            instance = replyForm.save(commit=False)
            instance.shop_id = shopInfo
            instance.review_id = reviewInfo
            instance.save()
            Review.objects.filter(id=reviewid).update(reply_by_vendor = True)
            ser_instance = serializers.serialize('json', [ instance, ])
            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            return JsonResponse({"error":replyForm.errors}, status=400)
    return JsonResponse({"error": " "}, status=400)



@csrf_exempt
def vendor_heart(request):
    if not request.user.is_authenticated:
        return render(request,"Account/account.html")
        
    if request.POST:
        reviewid = request.POST.get('reviewid')
        data = Review.objects.get(id=reviewid)
        val = data.heart_by_owner
        if val:
            Review.objects.filter(id=reviewid).update(heart_by_owner = False)
        else:
            Review.objects.filter(id=reviewid).update(heart_by_owner = True)
        return JsonResponse({"msg": "Review liked"}, status=200)

    else:
        return JsonResponse({"error": " "}, status=400)