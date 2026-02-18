from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = ('username', 'email', 'role', 'is_verified_employer', 'is_staff')
    list_filter = ('role', 'is_verified_employer')

    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {
            'fields': ('role', 'is_verified_employer'),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Information', {
            'fields': ('role', 'is_verified_employer'),
        }),
    )




