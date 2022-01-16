from django.db import models
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
    shop_area = models.CharField(verbose_name="Shop Area", max_length=50)
    shop_location = models.TextField(verbose_name="Shop Location", default=None)
    shop_tags = ArrayField(models.CharField(verbose_name="Shop Tags",max_length=50), blank=False)
    shop_logo = models.ImageField(verbose_name="Shop Logo",default='default.png', blank=True)
    shop_rating = models.FloatField(verbose_name="Shop Rating")
    shop_clicks_count = models.IntegerField(verbose_name="Shop Clicks Count")
    shop_wishlist_count = models.IntegerField(verbose_name="Shop Wishlist Count")
    shop_owner = models.ForeignKey(User,on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.shop_name

