from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _
from .validators import validate_iranian_phone_number
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserType(models.IntegerChoices):
    customer = 1, _("customer")
    admin = 2, _("admin")
    superuser = 3, _("superuser")


class ProfileGender(models.IntegerChoices):
    male = 1, _("male")
    female = 2, _("female")
    not_to_mention = 3, _("not to mention")


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        create and save user with email
        """
        if not email:
            raise ValueError(_("the email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        create and save super user with email
        """

        extra_fields.setdefault("is_verified", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("type", UserType.superuser.value)
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("is_staff must be True for Super user"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("is_superuser must be True for Super user"))
        if extra_fields.get("is_verified") is not True:
            raise ValueError(_("is_verified must be True for Super user"))
        # if extra_fields.get("type") is not UserType.superuser.value:
        #     raise ValueError(_("type must be superuser for Super user"))
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_verification_email = models.DateTimeField(null=True, blank=True)
    type = models.IntegerField(
        choices=UserType.choices, default=UserType.customer.value
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(
        "User", on_delete=models.CASCADE, related_name="user_profile"
    )
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    image = models.ImageField(
        upload_to="profile/", default="profile/default.jpg"
    )
    phone_number = models.CharField(
        max_length=12, validators=[validate_iranian_phone_number]
    )
    gender = models.IntegerField(
        choices=ProfileGender.choices, null=True, blank=True
    )
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def get_fullname(self):
        if self.first_name or self.last_name:
            return self.first_name + " " + self.last_name
        return "کاربر جدید"


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, pk=instance.pk)
