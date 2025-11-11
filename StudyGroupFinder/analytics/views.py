from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from groups.models import StudyGroup
from .utils import (
    calculate_group_analytics,
    update_member_activity,
    get_attendance_trends,
    get_member_growth_data,
    get_session_frequency_data,
    get_top_active_members
)
import json

@login_required
def group_analytics(request, group_id):
    """Display analytics dashboard for a group"""
    group = get_object_or_404(StudyGroup, pk=group_id)
    
    # Check if user is the creator
    if group.creator != request.user:
        messages.error(request, 'Only group creators can view analytics.')
        return redirect('groups:group_detail', pk=group_id)
    
    # Calculate/update analytics
    analytics = calculate_group_analytics(group)
    
    # Update member activities
    for member in group.members.all():
        update_member_activity(member, group)
    
    # Get chart data
    attendance_trends = get_attendance_trends(group, weeks=8)
    member_growth = get_member_growth_data(group, months=6)
    session_frequency = get_session_frequency_data(group, months=6)
    top_members = get_top_active_members(group, limit=5)
    
    # Get all member activities for detailed view
    from .models import MemberActivity
    all_members_activity = MemberActivity.objects.filter(
        group=group
    ).select_related('user').order_by('-activity_score')
    
    context = {
        'group': group,
        'analytics': analytics,
        'attendance_trends': json.dumps(attendance_trends),
        'member_growth': json.dumps(member_growth),
        'session_frequency': json.dumps(session_frequency),
        'top_members': top_members,
        'all_members_activity': all_members_activity,
    }
    
    return render(request, 'analytics/group_analytics.html', context)


@login_required
def refresh_analytics(request, group_id):
    """Manually refresh analytics for a group"""
    group = get_object_or_404(StudyGroup, pk=group_id, creator=request.user)
    
    # Recalculate analytics
    calculate_group_analytics(group)
    
    # Update all member activities
    for member in group.members.all():
        update_member_activity(member, group)
    
    messages.success(request, 'Analytics refreshed successfully!')
    return redirect('analytics:group_analytics', group_id=group_id)