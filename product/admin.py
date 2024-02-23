from django.contrib import admin
from . import models

# Register your models here.
class Size(admin.ModelAdmin):
    prepopulated_fields={'slug':('name',)}
    list_display=['name','slug']

class Color(admin.ModelAdmin):
    prepopulated_fields={'slug':('name',)}
    list_display=['name','slug']

class Category(admin.ModelAdmin):
    prepopulated_fields={'slug':('name',)}
    list_display=['name','slug']



admin.site.register(models.Product)
admin.site.register(models.Review)
admin.site.register(models.Size,Size)
admin.site.register(models.Color,Color)
admin.site.register(models.Category,Category)