from django.contrib import admin
from .models import StudyGroup, GroupMember, JoinRequest

@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'course_code', 'creator', 'group_type', 'current_member_count', 'max_capacity', 'created_at']
    list_filter = ['group_type', 'created_at']
    search_fields = ['name', 'course_name', 'course_code', 'creator__username']

@admin.register(GroupMember)
class GroupMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'group', 'role', 'joined_at']
    list_filter = ['role', 'joined_at']

@admin.register(JoinRequest)
class JoinRequestAdmin(admin.ModelAdmin):
    list_display = ['user', 'group', 'status', 'created_at']
    list_filter = ['status', 'created_at']