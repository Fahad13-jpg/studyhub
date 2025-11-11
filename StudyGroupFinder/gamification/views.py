from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserBadge, StudyStreak, UserPoints, Badge
from .utils import (
    check_and_award_badges,
    update_user_streak,
    check_achievements,
    get_user_gamification_data
)

@login_required
def achievements_page(request):
    """Display user's achievements, badges, and progress"""
    # Update user data
    check_and_award_badges(request.user)
    update_user_streak(request.user)
    check_achievements(request.user)
    
    # Get gamification data
    data = get_user_gamification_data(request.user)
    
    # Get all available badges
    all_badges = Badge.objects.all()
    earned_badge_ids = data['badges'].values_list('badge_id', flat=True)
    
    context = {
        'streak': data['streak'],
        'points': data['points'],
        'earned_badges': data['badges'],
        'all_badges': all_badges,
        'earned_badge_ids': earned_badge_ids,
        'achievements': data['achievements'],
        'badges_count': data['badges_count'],
        'achievements_count': data['achievements_count'],
    }
    
    return render(request, 'gamification/achievements.html', context)


@login_required
def leaderboard(request):
    """Display global leaderboard"""
    # Get filter type
    filter_type = request.GET.get('type', 'points')
    
    if filter_type == 'points':
        top_users = UserPoints.objects.select_related('user').order_by('-total_points')[:50]
    elif filter_type == 'streak':
        top_users = StudyStreak.objects.select_related('user').order_by('-current_streak')[:50]
    elif filter_type == 'badges':
        # Users with most badges
        from django.db.models import Count
        top_users = User.objects.annotate(
            badge_count=Count('earned_badges')
        ).order_by('-badge_count')[:50]
    else:
        top_users = UserPoints.objects.select_related('user').order_by('-total_points')[:50]
    
    context = {
        'top_users': top_users,
        'filter_type': filter_type,
    }
    
    return render(request, 'gamification/leaderboard.html', context)