from django.contrib import admin
from healthapp.models import product,Department

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display=['id','name','price','pdetails','cat','is_active']
    list_filter=['cat','price','is_active']
admin.site.register(product,ProductAdmin)
admin.site.register(Department)