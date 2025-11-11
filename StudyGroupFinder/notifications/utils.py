from django.urls import reverse
from .models import Notification, NotificationPreference

def create_notification(recipient, notification_type, title, message, **kwargs):
    """
    Create a new notification
    kwargs can include: group, session, join_request, actor, action_url
    """
    # Get or create user preferences
    prefs, created = NotificationPreference.objects.get_or_create(user=recipient)
    
    # Check if user wants this type of notification
    pref_map = {
        'session_reminder': prefs.inapp_session_reminders,
        'join_request': prefs.inapp_join_requests,
        'request_approved': prefs.inapp_request_responses,
        'request_rejected': prefs.inapp_request_responses,
        'new_member': prefs.inapp_new_members,
        'session_created': prefs.inapp_session_updates,
        'session_cancelled': prefs.inapp_session_updates,
    }
    
    # If user disabled this type, don't create
    if notification_type in pref_map and not pref_map[notification_type]:
        return None
    
    notification = Notification.objects.create(
        recipient=recipient,
        notification_type=notification_type,
        title=title,
        message=message,
        group=kwargs.get('group'),
        session=kwargs.get('session'),
        join_request=kwargs.get('join_request'),
        actor=kwargs.get('actor'),
        action_url=kwargs.get('action_url', '')
    )
    
    return notification


def notify_session_reminder(session):
    """Send reminder 24 hours before session to all attending members"""
    from user_sessions.models import SessionRSVP
    
    # Get all members who RSVP'd as attending or maybe
    attending_users = SessionRSVP.objects.filter(
        session=session,
        status__in=['attending', 'maybe']
    ).values_list('user', flat=True)
    
    for user_id in attending_users:
        from django.contrib.auth.models import User
        user = User.objects.get(id=user_id)
        
        create_notification(
            recipient=user,
            notification_type='session_reminder',
            title='📅 Session Reminder',
            message=f'Your study session "{session.title}" starts tomorrow at {session.time.strftime("%I:%M %p")}!',
            session=session,
            group=session.group,
            action_url=reverse('sessions:session_detail', kwargs={'pk': session.pk})
        )


def notify_join_request(join_request):
    """Notify group creator about new join request"""
    create_notification(
        recipient=join_request.group.creator,
        notification_type='join_request',
        title='👋 New Join Request',
        message=f'{join_request.user.get_full_name() or join_request.user.username} wants to join "{join_request.group.name}"',
        group=join_request.group,
        join_request=join_request,
        actor=join_request.user,
        action_url=reverse('groups:group_detail', kwargs={'pk': join_request.group.pk})
    )


def notify_request_approved(join_request):
    """Notify user that their join request was approved"""
    create_notification(
        recipient=join_request.user,
        notification_type='request_approved',
        title='✅ Request Approved!',
        message=f'Your request to join "{join_request.group.name}" has been approved!',
        group=join_request.group,
        join_request=join_request,
        action_url=reverse('groups:group_detail', kwargs={'pk': join_request.group.pk})
    )


def notify_request_rejected(join_request):
    """Notify user that their join request was rejected"""
    create_notification(
        recipient=join_request.user,
        notification_type='request_rejected',
        title='❌ Request Declined',
        message=f'Your request to join "{join_request.group.name}" was declined.',
        group=join_request.group,
        join_request=join_request
    )


def notify_new_member(group, new_member):
    """Notify all group members about new member"""
    for member in group.members.exclude(id=new_member.id):
        create_notification(
            recipient=member,
            notification_type='new_member',
            title='🎉 New Member',
            message=f'{new_member.get_full_name() or new_member.username} joined "{group.name}"',
            group=group,
            actor=new_member,
            action_url=reverse('groups:group_detail', kwargs={'pk': group.pk})
        )


def notify_session_created(session):
    """Notify all group members about new session"""
    for member in session.group.members.all():
        if member != session.created_by:
            create_notification(
                recipient=member,
                notification_type='session_created',
                title='📚 New Study Session',
                message=f'New session "{session.title}" scheduled for {session.date.strftime("%B %d")} in {session.group.name}',
                session=session,
                group=session.group,
                actor=session.created_by,
                action_url=reverse('user_sessions:session_detail', kwargs={'pk': session.pk})
            )


def notify_session_cancelled(session):
    """Notify all group members about cancelled session"""
    for member in session.group.members.all():
        create_notification(
            recipient=member,
            notification_type='session_cancelled',
            title='⚠️ Session Cancelled',
            message=f'Session "{session.title}" scheduled for {session.date.strftime("%B %d")} has been cancelled',
            session=session,
            group=session.group,
            action_url=reverse('sessions:group_sessions', kwargs={'group_id': session.group.pk})
        )


def notify_member_left(group, member):
    """Notify group creator when member leaves"""
    if group.creator != member:
        create_notification(
            recipient=group.creator,
            notification_type='member_left',
            title='👋 Member Left',
            message=f'{member.get_full_name() or member.username} left "{group.name}"',
            group=group,
            actor=member,
            action_url=reverse('groups:group_detail', kwargs={'pk': group.pk})
        )


def get_unread_count(user):
    """Get count of unread notifications for user"""
    return Notification.objects.filter(recipient=user, is_read=False).count()