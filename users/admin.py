from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email", "avatar", "phone", "country", "is_staff", "is_superuser", "is_active")
    search_fields = ("email", "country")
    ordering = ("email",)
    