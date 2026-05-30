from django.contrib import admin
from .models import ContactModel, NewsLetterModel


# Register your models here.
@admin.register(ContactModel)
class ContactModelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "phone_number",
        "subject",
        "is_seen",
        "created_date",
    )


@admin.register(NewsLetterModel)
class NewsLetterAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "created_date")
