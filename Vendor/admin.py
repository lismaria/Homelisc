from django.contrib import admin

# Register your models here.
import Vendor.models as Vm
admin.site.register(Vm.Shop)
admin.site.register(Vm.Item)
admin.site.register(Vm.Review)
admin.site.register(Vm.ItemImage)
admin.site.register(Vm.Wishlist)
admin.site.register(Vm.VendorReply)
admin.site.register(Vm.Category)