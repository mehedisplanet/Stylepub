from django.contrib import admin
from .models import ContactUs,Wishlist,Purchase,PurchaseHistory

# Register your models here.
admin.site.register(ContactUs)
admin.site.register(Wishlist)
admin.site.register(Purchase)
admin.site.register(PurchaseHistory)