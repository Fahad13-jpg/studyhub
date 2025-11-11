from django.db.models import Count, Q, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from .models import GroupAnalytics, MemberActivity, SessionAttendanceLog
from user_sessions.models import SessionRSVP

def calculate_group_analytics(group):
    """Calculate and cache analytics for a group"""
    analytics, created = GroupAnalytics.objects.get_or_create(group=group)
    
    # Member statistics
    analytics.total_members = group.members.count()
    
    # Calculate member growth rate (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    new_members = group.groupmember_set.filter(joined_at__gte=thirty_days_ago).count()
    analytics.member_growth_rate = (new_members / max(analytics.total_members, 1)) * 100
    
    # Session statistics
    all_sessions = group.sessions.all()
    analytics.total_sessions = all_sessions.count()
    analytics.completed_sessions = all_sessions.filter(
        date__lt=timezone.now().date(),
        is_cancelled=False
    ).count()
    analytics.cancelled_sessions = all_sessions.filter(is_cancelled=True).count()
    
    # Calculate average attendance rate
    completed_sessions = all_sessions.filter(date__lt=timezone.now().date(), is_cancelled=False)
    if completed_sessions.exists():
        total_possible_attendees = 0
        total_actual_attendees = 0
        
        for session in completed_sessions:
            total_possible_attendees += group.members.count()
            total_actual_attendees += SessionRSVP.objects.filter(
                session=session,
                status='attending'
            ).count()
        
        if total_possible_attendees > 0:
            analytics.average_attendance_rate = (total_actual_attendees / total_possible_attendees) * 100
    
    # Find most active member
    member_activities = MemberActivity.objects.filter(group=group).order_by('-activity_score').first()
    if member_activities:
        analytics.most_active_member = member_activities.user
        analytics.most_active_member_score = member_activities.activity_score
    
    # Time-based session statistics
    now = timezone.now()
    first_day_this_month = now.replace(day=1)
    first_day_last_month = (first_day_this_month - timedelta(days=1)).replace(day=1)
    
    analytics.sessions_this_month = all_sessions.filter(
        date__gte=first_day_this_month.date()
    ).count()
    
    analytics.sessions_last_month = all_sessions.filter(
        date__gte=first_day_last_month.date(),
        date__lt=first_day_this_month.date()
    ).count()
    
    analytics.save()
    return analytics


def update_member_activity(user, group):
    """Update activity metrics for a member"""
    activity, created = MemberActivity.objects.get_or_create(user=user, group=group)
    
    # Count sessions attended (with 'attending' RSVP)
    activity.sessions_attended = SessionRSVP.objects.filter(
        user=user,
        session__group=group,
        status='attending'
    ).count()
    
    # Count sessions created
    activity.sessions_created = group.sessions.filter(created_by=user).count()
    
    # Count messages sent
    try:
        from chat.models import GroupMessage
        activity.messages_sent = GroupMessage.objects.filter(
            sender=user,
            group=group
        ).count()
    except:
        activity.messages_sent = 0
    
    # Calculate and save activity score
    activity.calculate_activity_score()
    
    return activity


def get_attendance_trends(group, weeks=8):
    """Get attendance trends over time"""
    trends = []
    now = timezone.now()
    
    for week in range(weeks, 0, -1):
        week_start = now - timedelta(weeks=week)
        week_end = now - timedelta(weeks=week-1)
        
        sessions_in_week = group.sessions.filter(
            date__gte=week_start.date(),
            date__lt=week_end.date(),
            is_cancelled=False
        )
        
        if sessions_in_week.exists():
            total_attendees = 0
            total_possible = 0
            
            for session in sessions_in_week:
                total_possible += group.members.count()
                total_attendees += SessionRSVP.objects.filter(
                    session=session,
                    status='attending'
                ).count()
            
            attendance_rate = (total_attendees / max(total_possible, 1)) * 100
        else:
            attendance_rate = 0
        
        trends.append({
            'week': f"Week {weeks - week + 1}",
            'date': week_start.strftime('%b %d'),
            'rate': round(attendance_rate, 1)
        })
    
    return trends


def get_member_growth_data(group, months=6):
    """Get member growth over time"""
    growth_data = []
    now = timezone.now()
    
    for month in range(months, 0, -1):
        month_date = now - timedelta(days=30 * month)
        month_start = month_date.replace(day=1)
        
        members_count = group.groupmember_set.filter(
            joined_at__lte=month_start
        ).count()
        
        growth_data.append({
            'month': month_start.strftime('%b %Y'),
            'count': members_count
        })
    
    # Add current month
    growth_data.append({
        'month': now.strftime('%b %Y'),
        'count': group.members.count()
    })
    
    return growth_data


def get_session_frequency_data(group, months=6):
    """Get session frequency over time"""
    frequency_data = []
    now = timezone.now()
    
    for month in range(months, 0, -1):
        month_date = now - timedelta(days=30 * month)
        month_start = month_date.replace(day=1)
        if month > 1:
            month_end = (now - timedelta(days=30 * (month - 1))).replace(day=1)
        else:
            month_end = now
        
        sessions_count = group.sessions.filter(
            date__gte=month_start.date(),
            date__lt=month_end.date()
        ).count()
        
        frequency_data.append({
            'month': month_start.strftime('%b %Y'),
            'count': sessions_count
        })
    
    return frequency_data


def get_top_active_members(group, limit=5):
    """Get most active members with their statistics"""
    activities = MemberActivity.objects.filter(group=group).select_related('user').order_by('-activity_score')[:limit]
    
    members_data = []
    for activity in activities:
        members_data.append({
            'user': activity.user,
            'sessions_attended': activity.sessions_attended,
            'sessions_created': activity.sessions_created,
            'messages_sent': activity.messages_sent,
            'activity_score': activity.activity_score
        })
    
    return members_data