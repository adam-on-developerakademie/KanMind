from django.contrib import admin
from .models import Board

# Register your models here.


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    """
    Admin Interface for Board Model
    """
    list_display = ['title', 'owner', 'member_count', 'ticket_count', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title', 'owner__email', 'owner__fullname']
    filter_horizontal = ['members']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = [
        ('Grundinformationen', {
            'fields': ('title', 'owner')
        }),
        ('Mitglieder', {
            'fields': ('members',)
        }),
        ('Zeitstempel', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    ]
    
