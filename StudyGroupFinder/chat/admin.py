from django.contrib import admin
from .models import GroupMessage, MessageRead

@admin.register(GroupMessage)
class GroupMessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'group', 'message_preview', 'created_at', 'is_edited']
    list_filter = ['group', 'created_at', 'is_edited']
    search_fields = ['sender__username', 'message', 'group__name']
    date_hierarchy = 'created_at'
    
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message'

@admin.register(MessageRead)
class MessageReadAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'read_at']
    list_filter = ['read_at']