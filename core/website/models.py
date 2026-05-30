from django.db import models
from accounts.validators import validate_iranian_phone_number

# Create your models here.


class ContactModel(models.Model):
    full_name = models.CharField(max_length=250)
    phone_number = models.CharField(
        max_length=12,
        validators=[validate_iranian_phone_number],
        null=True,
        blank=True,
    )
    email = models.EmailField(max_length=255)
    subject = models.CharField(max_length=250)
    content = models.TextField(max_length=750)
    is_seen = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name


class NewsLetterModel(models.Model):
    email = models.EmailField(unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email
