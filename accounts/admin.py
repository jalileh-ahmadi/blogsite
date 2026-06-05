from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('تنظیمات شخصی', {'fields': ('allow_group_invites', 'bio', 'profile_image')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('تنظیمات شخصی', {'fields': ('allow_group_invites','bio', 'profile_image')}),
    )
