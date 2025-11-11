from django.contrib import admin
from .models import GroupAnalytics, MemberActivity, SessionAttendanceLog

@admin.register(GroupAnalytics)
class GroupAnalyticsAdmin(admin.ModelAdmin):
    list_display = ['group', 'total_members', 'total_sessions', 'average_attendance_rate', 'last_updated']
    list_filter = ['last_updated']
    search_fields = ['group__name']
    readonly_fields = ['last_updated']

@admin.register(MemberActivity)
class MemberActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'group', 'activity_score', 'sessions_attended', 'sessions_created', 'messages_sent']
    list_filter = ['group', 'last_activity']
    search_fields = ['user__username', 'group__name']
    ordering = ['-activity_score']

@admin.register(SessionAttendanceLog)
class SessionAttendanceLogAdmin(admin.ModelAdmin):
    list_display = ['session', 'user', 'attended', 'logged_at']
    list_filter = ['attended', 'logged_at']
    search_fields = ['user__username', 'session__title']