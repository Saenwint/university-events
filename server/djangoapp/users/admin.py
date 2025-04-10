from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User

class CustomUserAdmin(UserAdmin):
    # Убираем упоминания о username
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name')}),
        ('Права доступа', {
            'fields': ('is_active', 'is_staff', 'is_admin', 'is_superuser', 'is_confirmed'),
        }),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
        ('Дополнительно', {'fields': ('balance',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_admin', 'is_active')
    list_filter = ('is_admin', 'is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    filter_horizontal = ()

admin.site.register(User, CustomUserAdmin)