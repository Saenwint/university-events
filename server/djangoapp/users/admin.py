from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User

# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'email', 'first_name', 
        'last_name', 'is_admin', 
        'is_confirmed', 'balance'
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    list_filter = ('is_admin', 'is_confirmed')