from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models

# Register your models here.
@admin.register(models.User)
class CustomUserAdmin(UserAdmin):

    """Custom User Admin"""

    list_display = ("nickname","zzigsa" , "email_verified", "email_secret", "login_method") + UserAdmin.list_display

    list_filter = UserAdmin.list_filter + ("zzigsa",)

    fieldsets = UserAdmin.fieldsets + (
        (
            "Custom Profile",
            {
                "fields": ("zzigsa", "nickname")
            }
        ),
    )
