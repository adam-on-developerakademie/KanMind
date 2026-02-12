from django.contrib import admin
from .models import Task, Comment

# Register your models here.


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Admin Interface for Task Model
    """
    list_display = ['title', 'board', 'status', 'priority', 'assignee', 'reviewer', 'due_date', 'created_at']
    list_filter = ['status', 'priority', 'created_at', 'due_date', 'board']
    search_fields = ['title', 'description', 'board__title']
    readonly_fields = ['created_at', 'updated_at', 'comments_count']
    
    fieldsets = [
        ('Grundinformationen', {
            'fields': ('title', 'description', 'board', 'created_by')
        }),
        ('Status und Priorität', {
            'fields': ('status', 'priority', 'due_date')
        }),
        ('Zuweisungen', {
            'fields': ('assignee', 'reviewer')
        }),
        ('Statistiken', {
            'fields': ('comments_count',),
            'classes': ('collapse',)
        }),
        ('Zeitstempel', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    ]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin Interface for Comment Model
    """
    list_display = ['task', 'author', 'content_preview', 'created_at']
    list_filter = ['created_at', 'task__board']
    search_fields = ['content', 'author__fullname', 'task__title']
    readonly_fields = ['created_at']
    
    def content_preview(self, obj):
        """Short preview of comment content"""
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content
    content_preview.short_description = "Inhalt (Vorschau)"
    
