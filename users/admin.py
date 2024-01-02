
# Register your models here.
from .models import Client, Staff, APIUser
from django.contrib import admin
from users.models import User
from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea
from django.db import models


class UserAdminConfig(UserAdmin):
    model = User
    search_fields = ('email', 'full_name', )
    list_filter = ("id", 'email', 'full_name',
                   'is_active', 'is_staff')
    ordering = ('-start_date',)
    list_display = ("id", 'email', 'full_name',
                    'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'full_name',
         )}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})},
    }

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name',  'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )


admin.site.register(User, UserAdminConfig)
# admin.py


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'government_id',
                    'location', 'age', 'sex', 'phone', 'is_client']
    search_fields = ['name', 'government_id', 'location']
    list_filter = ['is_client']


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'department', 'shift', 'is_staff']
    search_fields = ['name', 'department', 'shift']
    list_filter = ['is_staff']


@admin.register(APIUser)
class APIUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'bank_name', 'api_user', 'email']
    search_fields = ['name', 'bank_name', 'email']
    list_filter = ['api_user']
