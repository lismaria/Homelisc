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

