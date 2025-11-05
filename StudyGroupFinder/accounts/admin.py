from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for UserProfile model
    """
    list_display = ['user', 'university', 'department', 'semester', 'year', 'created_at']
    list_filter = ['university', 'department', 'semester', 'year', 'created_at']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'university', 'department']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Academic Information', {
            'fields': ('university', 'department', 'semester', 'year')
        }),
        ('Personal Information', {
            'fields': ('phone', 'bio', 'profile_picture')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )