from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

# Register your models here.


User = get_user_model()

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin Interface für Custom User Model
    """
    list_display = ['email', 'fullname', 'username', 'is_active', 'is_staff', 'date_joined']
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'date_joined']
    search_fields = ['email', 'fullname', 'username']
    ordering = ['email']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Zusätzliche Informationen', {'fields': ('fullname',)}),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Zusätzliche Informationen', {'fields': ('fullname', 'email')}),
    )