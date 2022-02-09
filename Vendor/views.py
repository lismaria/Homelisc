from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F, Avg, Sum, Count
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from Vendor.models import Category, Item, Review, Shop, ItemImage, VendorReply, Wishlist
from Account.models import User
from Vendor.forms import ReplyPostForm, ShopCreationForm, ItemCreationForm, ItemImageUploadForm, ItemImageEditForm
from Account.forms import AccountUpdationForm

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



def home(request):

    if not request.user.is_authenticated:
        categories = Category.objects.all()
        shops = Shop.objects.order_by(F('shop_rating').desc(nulls_last=True),F('shop_wishlist_count').desc(nulls_last=True))[:6]
        topcats = Category.objects.order_by('-category_count')[:10]
        bestpicks = Item.objects.order_by(F('item_rating').desc(nulls_last=True),F('item_wishlist_count').desc(nulls_last=True))[:4]
        return render(request,'home.html',{'shops':shops,'categories':categories, 'topcats':topcats, 'bestpicks':bestpicks})

    elif (request.user.is_authenticated and request.user.is_vendor == True):
        vendorForm = AccountUpdationForm(initial={'name':request.user.name,'email':request.user.email})
        shopInfo = Shop.objects.filter(shop_owner_id=request.user.id)
        shopCount = shopInfo.count()
        
        if shopCount == 0:
            return render(request,'Vendor/perks.html')
        else:
            return render(request,'Vendor/home.html',{'shopInfo':shopInfo,'shopCount':shopCount,'vendorForm':vendorForm})
    
    else:
        categories = Category.objects.all()
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
        return render(request,'home.html',{'shops':shops,'categories':categories, 'topcats':topcats, 'usershopwish':usershopwish, 'useritemwish':useritemwish, 'bestpicks':bestpicks})



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

    # reviewGrp = Review.objects.filter(shop_id=id)
    # reviewVal = reviewGrp.values('date')
    # reviewAno = reviewVal.annotate(Avg('stars'))
    # print("reviewGrp: ",reviewGrp)
    # print("reviewVal: ",reviewVal)
    # print("reviewAno: ",reviewAno)

    # for i in reviewAno:
    #     print(i['date'].strftime('%m/%d/%Y'))
    #     print(i['date'].strftime("%A"))

    # Sales.objects
    #     .annotate(month=TruncMonth('created'))  # Truncate to month and add to select list
    #     .values('month')                          # Group By month
    #     .annotate(c=Count('id'))                  # Select the count of the grouping
    #     .values('month', 'c')                     # (might be redundant, haven't tested

    # reviewGrp = Review.objects.filter(shop_id=id)
    # reviewAno1 = reviewGrp.annotate(day=TruncDay('date'))
    # reviewVal = reviewAno1.values('day')
    # reviewAno2 = reviewVal.annotate(Avg('stars'))

    # print("\nreviewGrp: ",reviewGrp)
    # print("\nreviewAno1: ",reviewAno1)
    # print("\nreviewVal: ",reviewVal)
    # print("\nreviewAno2: ",reviewAno2)
    
    # for i in reviewAno2:
    #     print(i['day'].strftime('%m/%d/%Y'))
    #     print(i['day'].strftime("%A"))
    #     print(i['stars__avg'])
    #     print("\n")
    

    # reviewGrp = Review.objects.filter(shop_id=id).values()
    # print(reviewGrp)
    # df = pd.DataFrame(reviewGrp)
    # print(df[['date','stars']])

    # # df.set_index('date', inplace = True)
    # ind = pytz.timezone('Asia/Kolkata')
    # # df.index = df.index.tz_convert(ind)
    # df['date'] = df['date'].dt.tz_convert(ind)
    # print(df[['date','stars']])
    # df['date'] = df['date'].dt.strftime('%d-%m-%Y')
    # # print(df)
    # print(df[['date','stars']])
    


    shopForm = ShopCreationForm(initial={'shop_name':shop_details[0]['shop_name'],'shop_tags':shop_details[0]['shop_tags'],'shop_descr':shop_details[0]['shop_descr'],'shop_contact':shop_details[0]['shop_contact'],'shop_state':shop_details[0]['shop_state'],'shop_city':shop_details[0]['shop_city'],'shop_location':shop_details[0]['shop_location'],'shop_logo':shop_details[0]['shop_logo']})
    obj = get_object_or_404(Shop, pk=id)
    if obj.shop_slug != slug:
        return redirect('vendor:shop', id=obj.pk, slug=obj.shop_slug)
    return render(request,"Vendor/shop.html",{'shopInfo':shopInfo,'vendorForm':vendorForm,'shopForm':shopForm})



def shop_insights(request):
    shopid = request.GET['shopid']

    # Shop rating pie chart 
    shopRating = Review.objects.filter(shop_id=shopid).values('stars').annotate(Count('stars')).order_by('-stars')
    shopRatingPie = []
    for i in shopRating:
        shopRatingPie.append(i['stars__count'])

    # Item Wihslist/Visit Count
    itemwishclick = Item.objects.filter(shop_id=shopid).values_list('item_name','item_wishlist_count','item_clicks_count').order_by('item_name')
    print(itemwishclick)
    wishclick_item_name = []
    item_wish_count = []
    item_click_count = []
    for i in itemwishclick:
        # if not (i[1]==0 and i[2]==0):
        wishclick_item_name.append(i[0])
        item_wish_count.append(i[1])
        item_click_count.append(i[2])

    
    return render(request, "Vendor/insights.html", {'shopRatingPie': shopRatingPie,'wishclick_item_name':wishclick_item_name,'item_wish_count':item_wish_count,'item_click_count':item_click_count})



def menu_view(request,id,slug):
    shopobj = check_vendor_details(request,id)
    itemInfo = Item.objects.filter(shop_id=id).order_by('-id')
    imageInfo = ItemImage.objects.filter(shop_id=id)
    itemForm = ItemCreationForm()
    imageForm = ItemImageUploadForm()
    itemcount = itemInfo.count()
    if shopobj==None:
        return redirect("home")
    obj = get_object_or_404(Shop, pk=id)
    if obj.shop_slug != slug:
        return redirect('vendor:shop', id=obj.pk, slug=obj.shop_slug)
    return render(request,"Vendor/menu.html",{'shopInfo':shopobj['shopInfo'],'vendorForm':shopobj['vendorForm'],'itemForm':itemForm, 'imageForm':imageForm, 'itemInfo':itemInfo, 'imageInfo':imageInfo,'itemcount':itemcount})



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
        files = request.FILES.getlist('item_img')

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
        else:
            return JsonResponse({"error": imageForm.errors}, status=400)
            
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
        return JsonResponse({"instance": ser_instance}, status=200)
        
    else:
        itemid=request.GET.get('id')
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
        
        return render(request, 'Vendor/itemedit.html',{'itemid':itemid,'imageForm':imageForm,'filledItemForm':filledItemForm, 'imageCombo':imageCombo})
    return JsonResponse({"error": " ", }, status=400)



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