from django.shortcuts import render
from django.db import models
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.db.models import Count, Q, F
from groups.models import StudyGroup
from user_sessions.models import StudySession, SessionRSVP

@login_required
def dashboard(request):
    """Personalized dashboard for logged-in users"""
    user = request.user
    
    # Get user's groups
    created_groups = user.created_groups.all()
    joined_groups = user.joined_groups.exclude(creator=user)
    all_my_groups = user.joined_groups.all()
    
    # Get upcoming sessions for current week
    today = datetime.now().date()
    week_end = today + timedelta(days=7)
    
    upcoming_sessions = StudySession.objects.filter(
        group__in=all_my_groups,
        date__gte=today,
        date__lte=week_end,
        is_cancelled=False
    ).select_related('group', 'created_by').order_by('date', 'time')[:10]
    
    # Get user's RSVP status for upcoming sessions
    from user_sessions.models import SessionRSVP
    user_rsvps = SessionRSVP.objects.filter(
        user=user,
        session__in=upcoming_sessions
    ).values_list('session_id', 'status')
    rsvp_dict = dict(user_rsvps)
    
    # Get recommended groups (public groups user hasn't joined)
    recommended_groups = StudyGroup.objects.filter(
        group_type='public'
    ).exclude(
        members=user
    ).annotate(
        member_count=Count('members')
    ).filter(
        member_count__lt=models.F('max_capacity')
    ).order_by('-created_at')[:6]
    
    # Calculate statistics
    total_groups_joined = all_my_groups.count()
    total_groups_created = created_groups.count()
    
    # Count sessions attended (RSVPs with 'attending' status)
    total_sessions_attended = SessionRSVP.objects.filter(
        user=user,
        status='attending'
    ).count()
    
    # Count total sessions in user's groups
    total_sessions_scheduled = StudySession.objects.filter(
        group__in=all_my_groups
    ).count()
    
    context = {
        'created_groups': created_groups[:5],  # Show max 5
        'joined_groups': joined_groups[:5],    # Show max 5
        'upcoming_sessions': upcoming_sessions,
        'rsvp_dict': rsvp_dict,
        'recommended_groups': recommended_groups,
        'total_groups_joined': total_groups_joined,
        'total_groups_created': total_groups_created,
        'total_sessions_attended': total_sessions_attended,
        'total_sessions_scheduled': total_sessions_scheduled,
    }
    
    return render(request, 'dashboard/dashboard.html', context)