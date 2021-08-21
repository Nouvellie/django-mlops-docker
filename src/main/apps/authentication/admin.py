from .models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin


class UserAdminConfig(UserAdmin):
    """This class allows you to manage the User model, from the Django admin menu."""

    ordering = ['-created_at']
    list_display = ('username', 'email', 'is_active',
                    'is_verified', 'is_staff', 'is_superuser', 'acc_hash')
    list_filder = ('username', 'email', 'is_active',
                   'is_verified', 'is_staff', 'is_superuser', 'acc_hash')
    search_fields = ('username', 'email')

    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email')}),
        ('Permission', {'fields': ('is_active',
                                   'is_verified', 'is_staff', 'is_superuser', 'acc_hash')}),
        ('Dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'password1', 'password2', 'is_active', 'is_verified', 'is_staff', 'acc_hash')}
         ),
    )


admin.site.register(User, UserAdminConfig)
