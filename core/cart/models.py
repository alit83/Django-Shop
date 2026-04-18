from django.db import models

# Create your models here.
class CartModel(models.Model):
    user=models.ForeignKey("accounts.User",on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def calculate_total_price(self):
        return  sum(item.product.get_price() * item.quantity for item in self.cart_items.all())

class CartItemModel(models.Model):
    cart = models.ForeignKey(CartModel,on_delete=models.CASCADE,related_name="cart_items")
    product = models.ForeignKey("shop.Product",on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

