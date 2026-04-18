from django.contrib import admin
from .models import PaymentModel

# Register your models here.


@admin.register(PaymentModel)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "authority_id",
        "amount",
        "ref_id",
        "status",
        "created_date"
    )
