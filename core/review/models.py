from django.db import models
from shop.models import Product
from django.core.validators import MaxValueValidator, MinValueValidator
from django.dispatch import receiver
from django.db.models.signals import post_save , pre_save
from django.db.models import Avg
# Create your models here.

class ReviewStatus(models.IntegerChoices):
    pending = 1 , "در انتظار تایید"
    accepted = 2 ,"تایید شده"
    rejected = 3 ,"رد شده"

class ReviewModel(models.Model):
    user = models.ForeignKey('accounts.User' , on_delete=models.PROTECT)
    product = models.ForeignKey('shop.Product',on_delete=models.CASCADE)
    description = models.TextField()
    rate = models.IntegerField(default=5 , validators=[MinValueValidator(0),MaxValueValidator(5)])
    status = models.IntegerField(
        choices=ReviewStatus.choices, default=ReviewStatus.pending.value)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def get_status(self):
        return {
            "id":self.status,
            "title":ReviewStatus(self.status).name,
            "label":ReviewStatus(self.status).label,
        }



@receiver(pre_save, sender=ReviewModel)
def calculate_avg_review(sender, instance, **kwargs):
    if not instance.pk:
        return   # new object; nothing changed yet

    old_value = sender.objects.get(pk=instance.pk).status
    new_value = instance.status

    if old_value == new_value or (old_value==ReviewStatus.pending.value and new_value==ReviewStatus.rejected.value):
        return
    product = instance.product
    reviews= ReviewModel.objects.filter(product=product, status=ReviewStatus.accepted)
    rates = list(reviews.values_list("rate", flat=True))
    if new_value == ReviewStatus.accepted.value:
        rates.append(instance.rate)
    else:
        rates.remove(instance.rate)
    avg = sum(rates) / len(rates) if rates else 0
    product.avg_rate = round(avg,1)
    product.save()

    #user = instance.user