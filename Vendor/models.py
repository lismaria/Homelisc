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
    shop_tags = ArrayField(models.CharField(verbose_name="Shop Tags",max_length=50),size=3, blank=False)
    shop_logo = models.ImageField(verbose_name="Shop Logo",default='default-shop.svg', blank=True)
    shop_rating = models.DecimalField(verbose_name="Shop Rating",null=True, blank=True, default=None, max_digits=2, decimal_places=1)
    shop_clicks_count = models.IntegerField(verbose_name="Shop Clicks Count",null=True, blank=True, default=0)
    shop_wishlist_count = models.IntegerField(verbose_name="Shop Wishlist Count",null=True, blank=True, default=0)
    shop_owner = models.ForeignKey(User,on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.shop_name
    
    def save(self, *args, **kwargs):
        self.shop_slug = slugify(self.shop_name)
        super(Shop, self).save(*args, **kwargs)

class Item(models.Model):
    item_name = models.CharField(verbose_name="Item Name", max_length=50)
    item_descr = models.TextField(verbose_name="Item Description")    
    item_rating = models.DecimalField(verbose_name="Item Rating",null=True, default=None, max_digits=2, decimal_places=1)
    item_price = models.DecimalField(verbose_name="Item Price", max_digits=15, decimal_places=2)
    item_clicks_count = models.IntegerField(verbose_name="Item Clicks Count",null=True, blank=True, default=0)
    item_wishlist_count = models.IntegerField(verbose_name="Item Wishlist Count",null=True, blank=True, default=0)
    item_category = ArrayField(models.CharField(verbose_name="Item Category",max_length=50), size=3, blank=False)
    item_img_def = models.ImageField(verbose_name="Item Image Default",default="default-item.svg",blank=True)
    shop_id = models.ForeignKey(Shop,on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.item_name

class ItemImage(models.Model):
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE, default=None)
    shop_id = models.ForeignKey(Shop,on_delete=models.CASCADE, default=None)
    item_img = models.ImageField(verbose_name="Item Image", blank=True)

    def __str__(self):
        return self.item_id.item_name


class Review(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE, default=None)
    comment = models.TextField(verbose_name="Comment")
    stars = models.IntegerField(verbose_name="Stars")
    date = models.DateTimeField(auto_now_add=True)
    # likes = models.IntegerField(verbose_name="Likes", null=True, blank=True, default=0)
    likes = models.ManyToManyField(User,related_name='review_like',verbose_name="Likes")
    heart_by_owner = models.BooleanField(default=False)
    review_img = models.ImageField(verbose_name="Review Image", null=True, blank=True, default=None)
    shop_id = models.ForeignKey(Shop, on_delete=models.CASCADE, default=None)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True, default=None)
    reply_by_vendor = models.BooleanField(default=False)

    def __str__(self):
        return self.user_id.email

    def likes_count(self):
        return self.likes.count()

class Wishlist(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    shop_id = models.ForeignKey(Shop, on_delete=models.CASCADE, default=None)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
        return self.user_id.email +" "+ self.shop_id.shop_name

class VendorReply(models.Model):
    reply = models.TextField(verbose_name="Reply")
    date = models.DateTimeField(auto_now_add=True)
    shop_id = models.ForeignKey(Shop, on_delete=models.CASCADE, default=None)
    review_id = models.ForeignKey(Review, on_delete=models.CASCADE, default=None)
    
    def __str__(self):
        return self.shop_id.shop_name

class Category(models.Model):
    category_name = models.CharField(verbose_name="Category Name",max_length=50, blank=False, unique=True)
    category_descr = models.TextField(verbose_name="Category Description",null=True,blank=True,default=None)
    category_img = models.ImageField(verbose_name="Category Image",blank=True,default="default-category.svg")
    category_count = models.IntegerField(verbose_name="Category Count",null=True, blank=True, default=1)

    def __str__(self):
        return self.category_name

class Theme(models.Model):
    theme = models.CharField(verbose_name="Theme",max_length=50)
    date = models.DateField()

    def __str__(self):
        return self.theme