from django.contrib import admin
from cart.models import CartModel , CartItemModel
# Register your models here.
@admin.register(CartModel)
class CartAdmin(admin.ModelAdmin):
    list_display = ["user",]
@admin.register(CartItemModel)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ["cart","product","quantity"]

