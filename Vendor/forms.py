from dataclasses import fields
from django import forms
import Vendor.models as Vendor

class ItemCreationForm(forms.ModelForm):
    class Meta:
        model = Vendor.Item
        fields = ['item_name', 'item_descr', 'item_price', 'item_category']
        widgets = {
            'item_name' : forms.TextInput(attrs={'placeholder':'Item Name'}), 
            'item_descr' : forms.Textarea(attrs={'placeholder':'Item Description'}), 
            'item_price' : forms.NumberInput(attrs={'placeholder':'Item Price'}), 
            'item_category' : forms.TextInput(attrs={'placeholder':'Category (eg. Wall Painting, Brownies,..)'})
        }

# class ItemImageUploadForm(ItemCreationForm):
#     # item_img = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),required=False)
#     class Meta(ItemCreationForm.Meta):
#         fields = ItemCreationForm.Meta.fields + ['item_img',]
#         widgets = {
#             'item_img': forms.ClearableFileInput(attrs={'multiple': True})
#         }
#         # required= {
#         #     'item_img': False
#         # }

class ItemImageUploadForm(forms.ModelForm):
    # item_img = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),required=False)
    class Meta:
        model = Vendor.ItemImage
        fields = ('item_img',)
        widgets = {
            'item_img': forms.ClearableFileInput(attrs={'type':'file' ,'id':'add-itemimg','style':'display:none', 'accept':'image/png, image/jpeg'})
        }
        # required= {
        #     'item_img': False
        # }

class ItemImageEditForm(forms.ModelForm):
    # item_img = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),required=False)
    class Meta:
        model = Vendor.ItemImage
        fields = ('item_img',)
        widgets = {
            'item_img': forms.ClearableFileInput(attrs={'type':'file' ,'id':'edit-itemimg','style':'display:none', 'accept':'image/png, image/jpeg'})
        }

class ShopCreationForm(forms.ModelForm):
    class Meta:
        model = Vendor.Shop
        fields = ['shop_name', 'shop_tags', 'shop_descr', 'shop_contact', 'shop_state', 'shop_city', 'shop_location', 'shop_logo']
        labels = {
            'shop_name': '',
            'shop_tags': '', 
            'shop_descr': '',
            'shop_contact': '',
            'shop_state': '',
            'shop_city': '',
            'shop_location': '',
            'shop_logo': '',
        }
        widgets = {
            'shop_name': forms.TextInput(attrs={'placeholder':'Shop Name'}),
            'shop_tags': forms.TextInput(attrs={'placeholder':'Tags (eg. Chocolates,Crafts,..)'}),
            'shop_descr': forms.Textarea(attrs={'placeholder':'Shop Description'}),
            'shop_contact': forms.TextInput(attrs={'placeholder':'Shop Contact Number','pattern':'^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$'}),
            'shop_state': forms.Select(attrs={'id':'select-state'}),
            'shop_city': forms.Select(attrs={'id':'select-city'}),
            'shop_location': forms.TextInput(attrs={'placeholder':'Add Location',"style":"width:60%;height:100%"}),
            'shop_logo': forms.FileInput(attrs={"id":"add_logo", "style":"display:none;", "onchange":"document.getElementById('logo_pic').src = window.URL.createObjectURL(this.files[0])", "accept":"image/png, image/jpeg"}),
        }

class ReviewForm(forms.ModelForm):
    CHOICES = [(1,1), (2,2), (3,3), (4,4), (5,5)]
    stars = forms.CharField(label='What is your favorite fruit?', widget=forms.RadioSelect(choices=CHOICES, attrs={'class':'star','name':'star','ng-model':"stars",'ng-required':'true'}))
    class Meta:
        model = Vendor.Review
        fields = ['comment','stars','review_img']
        labels = {
            'comment':'',
            'review_img':'',
        }
        widgets = {
            'comment': forms.Textarea(attrs={'placeholder':'Share your experience...', 'ng-model':"comment",'ng-required':'true'}),
            'review_img': forms.ClearableFileInput(attrs={'type':'file','id':'add-pic','style':'display:none','onchange':'document.getElementById("review_pic").src = window.URL.createObjectURL(this.files[0])','accept':'image/png, image/jpeg'}),
        }

class ReplyPostForm(forms.ModelForm):
    class Meta:
        model = Vendor.VendorReply
        fields = ['reply']
        labels = {
            'reply': '',
        }
        widgets = {
            'reply': forms.Textarea(attrs={'placeholder':'Your Reply...'})
        }