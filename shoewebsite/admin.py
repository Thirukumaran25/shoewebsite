from django.contrib import admin
from .models import *
# Register your models here.

# homepage
admin.site.register(Logo)
admin.site.register(Banner)
admin.site.register(Homecategory)
admin.site.register(Homeproduct)

# homepage
admin.site.register(Contact)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price_mrp", "rating")
    search_fields = ("name",)

@admin.register(MenProduct)
class MenProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price_mrp", "rating")
    search_fields = ("name",)

@admin.register(KidProduct)
class KidProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price_mrp", "rating")
    search_fields = ("name",)