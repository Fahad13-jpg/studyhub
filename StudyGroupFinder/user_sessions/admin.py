from django.contrib import admin
from .models import StudySession, SessionRSVP

@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'group', 'date', 'time', 'location', 'created_by', 'is_cancelled']
    list_filter = ['is_cancelled', 'date', 'group']
    search_fields = ['title', 'group__name', 'created_by__username']
    date_hierarchy = 'date'

@admin.register(SessionRSVP)
class SessionRSVPAdmin(admin.ModelAdmin):
    list_display = ['user', 'session', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['user__username', 'session__title']