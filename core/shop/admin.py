from django.contrib import admin
from shop.models import (Product , ProductCategory , ProductImage , WishlistProductModel , ProductAttribute , Attribute , AttributeGroup)
# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['id','user','category','title','stock','status','created_date']

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display=['id','title','parent']

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display=['id','file']

@admin.register(WishlistProductModel)
class WishlistProductAdmin(admin.ModelAdmin):
    list_display=['user','product']

@admin.register(AttributeGroup)
class AttributeGroupAdmin(admin.ModelAdmin):
    list_display=['id','title','category']

@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display=['id','title','group']

@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    list_display=['id','product','attribute','value']


    
