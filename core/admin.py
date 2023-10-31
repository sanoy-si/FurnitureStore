from Store.models import Product
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from Store.admin import ProductAdmin, ProductImageInline
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2","email","first_name","last_name","phone_no"),
            },
        ),
    )
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (("Personal info"), {"fields": ("first_name", "last_name", "email","phone_no")}),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

class CustomProductAdmin(ProductAdmin):
    inlines = [ProductImageInline]

