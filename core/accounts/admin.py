from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import Profile
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
User = get_user_model()


# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ["email", "is_active", "is_superuser"]
    list_filter = ["email", "is_active", "is_superuser"]
    search_fields = ("email",)
    ordering = ("email",)
    fieldsets = (
        (
            "Authentication",
            {
                "fields": ("email", "password"),
            },
        ),
        (
            "permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_verified",
                ),
            },
        ),
        (
            "group_permissions",
            {
                "fields": ("groups", "user_permissions", "type"),
            },
        ),
        (
            "important_dates",
            {
                "fields": ("last_login",),
            },
        ),
    )
    add_fieldsets = (
        (
            "create_User",
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "is_verified",
                    "type",
                ),
            },
        ),
    )


class ProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "gender", "phone_number"]
    search_fields = ("user",)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()

    list_display = ["session_key", "_session_data", "expire_date"]
    readonly_fields = ["_session_data"]


admin.site.register(Session, SessionAdmin)
