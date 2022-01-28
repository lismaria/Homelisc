from django.db import models
from django.template.defaultfilters import slugify
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.postgres.fields import ArrayField
from Account.models import User
# Create your models here.

#  Id(PK)	Name	Contact	City	Area	Location	Tags	Logo	Description	Owner(FK)	Rating	Click Rates	Wishlist_count	

class Shop(models.Model):
    shop_name = models.CharField(verbose_name="Shop Name", max_length=50)
    shop_slug = models.SlugField()
    shop_descr = models.TextField(verbose_name="Shop Description")    
    shop_contact = PhoneNumberField(null=False, blank=False)
    shop_city = models.CharField(verbose_name="Shop City", max_length=50)
    shop_state = models.CharField(verbose_name="Shop State", max_length=50)
    shop_location = models.TextField(verbose_name="Shop Location", default=None)
    shop_tags = ArrayField(models.CharField(verbose_name="Shop Tags",max_length=50), blank=False)
    shop_logo = models.ImageField(verbose_name="Shop Logo",default='default.png', blank=True)
    shop_rating = models.FloatField(verbose_name="Shop Rating",null=True, default=None)
    shop_clicks_count = models.IntegerField(verbose_name="Shop Clicks Count",null=True, default=None)
    shop_wishlist_count = models.IntegerField(verbose_name="Shop Wishlist Count",null=True, default=None)
    shop_owner = models.ForeignKey(User,on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.shop_name
    
    def save(self, *args, **kwargs):
        self.shop_slug = slugify(self.shop_name)
        super(Shop, self).save(*args, **kwargs)

class Item(models.Model):
    item_name = models.CharField(verbose_name="Item Name", max_length=50)
    item_descr = models.TextField(verbose_name="Item Description")    
    item_rating = models.FloatField(verbose_name="Item Rating",null=True, default=None)
    item_price = models.FloatField(verbose_name="Item Price")
    item_clicks_count = models.IntegerField(verbose_name="Item Clicks Count",null=True, default=None)
    item_wishlist_count = models.IntegerField(verbose_name="Item Wishlist Count",null=True, default=None)
    item_category = ArrayField(models.CharField(verbose_name="Item Category",max_length=50), blank=False)
    shop_id = models.ForeignKey(Shop,on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.item_name

class ItemImage(models.Model):
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE, default=None)
    shop_id = models.ForeignKey(Shop,on_delete=models.CASCADE, default=None)
    item_img = models.ImageField(verbose_name="Item Image", blank=True)

    def __str__(self):
        return self.item_id.item_name

class ShopReview(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE, default=None)
    comment = models.TextField(verbose_name="Comment")
    stars = models.IntegerField(verbose_name="Stars")
    date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(verbose_name="Likes")
    heart_by_owner = models.BooleanField(default=False)
    shop_review_img = models.ImageField(verbose_name="Shop Review Image", default=None)
    shop_id = models.ForeignKey(Shop,on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.user_id.email


class ItemReview(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE, default=None)
    comment = models.TextField(verbose_name="Comment")
    stars = models.IntegerField(verbose_name="Stars")
    date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(verbose_name="Likes")
    heart_by_owner = models.BooleanField(default=False)
    item_review_img = models.ImageField(verbose_name="Item Review Image", default=None)
    shop_id = models.ForeignKey(Shop, on_delete=models.CASCADE, default=None)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.user_id.email


class ShopWishlist(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    shop_id = models.ForeignKey(Shop, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.shop_id.shop_name +" "+ self.user_id.email

class ItemWishlist(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    shop_id = models.ForeignKey(Shop, on_delete=models.CASCADE, default=None)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.item_id.item_name +" "+ self.user_id.email
