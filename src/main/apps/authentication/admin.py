from .models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


class UserAdminConfig(UserAdmin):
    ordering = ['-created_at']
    list_display = ('email', 'username', 'is_active',
                    'is_verified', 'is_staff', 'is_superuser')
    list_filder = ('email', 'username', 'is_active',
                   'is_verified', 'is_staff', 'is_superuser')
    search_fields = ('email', 'username')

    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name',)}),
        ('Permission', {'fields': ('is_active',
                                   'is_verified', 'is_staff', 'is_superuser',)}),
        ('Dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'password1', 'password2', 'is_active', 'is_verified', 'is_staff')}
         ),
    )


admin.site.register(User, UserAdminConfig)
