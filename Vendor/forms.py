from dataclasses import fields
from django import forms
import Vendor.models as Vendor

class ItemCreationForm(forms.ModelForm):
    class Meta:
        model = Vendor.Item
        fields = ['item_name', 'item_descr', 'item_price', 'item_category']

class ItemImageUploadForm(ItemCreationForm):
    # item_img = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),required=False)
    class Meta(ItemCreationForm.Meta):
        fields = ItemCreationForm.Meta.fields + ['item_img',]
        widgets = {
            'item_img': forms.ClearableFileInput(attrs={'multiple': True})
        }
        # required= {
        #     'item_img': False
        # }

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
            'shop_contact': forms.TextInput(attrs={'placeholder':'Shop Contact Number'}),
            'shop_state': forms.Select(attrs={'placeholder':'State'}),
            'shop_city': forms.Select(attrs={'placeholder':'City'}),
            'shop_location': forms.TextInput(attrs={'placeholder':'Add Location'}),
            'shop_logo': forms.FileInput(attrs={"id":"add_logo", "style":"display:none;", "onchange":"document.getElementById('logo_pic').src = window.URL.createObjectURL(this.files[0])", "accept":"image/*"}),
        }

