from django.dispatch import receiver
from django.db.models.signals import pre_save
from order.models import OrderModel, OrderStatusType


@receiver(pre_save, sender=OrderModel)
def reduce_stock(sender, instance, **kwargs):
    if instance.status == OrderStatusType.success.value:
        for item in instance.order_items.all():
            product_obj = item.product
            product_obj.stock = product_obj.stock - item.quantity
            product_obj.save()
    return
