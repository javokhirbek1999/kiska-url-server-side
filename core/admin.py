from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from . import models


class UserAdmin(UserAdmin):
    ordering = ['id']
    list_display = ['email','date_joined','date_updated']
    fieldsets = (
        (None, {'fields': ('email',)}),
        (_('Permissions'), {'fields': ('is_active','is_staff','is_superuser')}),
        (_('Important Dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )

admin.site.register(models.User, UserAdmin)