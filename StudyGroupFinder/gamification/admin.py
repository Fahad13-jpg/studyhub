from django.contrib import admin
from .models import Badge, UserBadge, StudyStreak, UserPoints, Achievement, UserAchievement

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['name', 'badge_type', 'tier', 'points', 'requirement_value']
    list_filter = ['badge_type', 'tier']
    search_fields = ['name', 'description']

@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ['user', 'badge', 'earned_at']
    list_filter = ['badge__badge_type', 'earned_at']
    search_fields = ['user__username', 'badge__name']
    date_hierarchy = 'earned_at'

@admin.register(StudyStreak)
class StudyStreakAdmin(admin.ModelAdmin):
    list_display = ['user', 'current_streak', 'longest_streak', 'total_sessions_attended', 'last_activity_date']
    list_filter = ['last_activity_date']
    search_fields = ['user__username']
    ordering = ['-current_streak']

@admin.register(UserPoints)
class UserPointsAdmin(admin.ModelAdmin):
    list_display = ['user', 'level', 'total_points', 'points_from_badges', 'points_from_sessions']
    list_filter = ['level']
    search_fields = ['user__username']
    ordering = ['-total_points']

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ['name', 'requirement_type', 'requirement_value', 'points_reward', 'is_hidden']
    list_filter = ['requirement_type', 'is_hidden']
    search_fields = ['name', 'description']

@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ['user', 'achievement', 'progress', 'earned_at']
    list_filter = ['earned_at']
    search_fields = ['user__username', 'achievement__name']
    date_hierarchy = 'earned_at'