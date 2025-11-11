from django import template
from gamification.models import UserBadge, UserPoints, StudyStreak

register = template.Library()

@register.simple_tag
def get_user_badges(user):
    """Get user's earned badges"""
    return UserBadge.objects.filter(user=user).select_related('badge')[:6]

@register.simple_tag
def get_user_points(user):
    """Get user's points and level"""
    points, created = UserPoints.objects.get_or_create(user=user)
    return points

@register.simple_tag
def get_user_streak(user):
    """Get user's study streak"""
    streak, created = StudyStreak.objects.get_or_create(user=user)
    return streak