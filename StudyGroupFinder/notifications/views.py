from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Notification, NotificationPreference
from .utils import get_unread_count

@login_required
def notifications_list(request):
    """Display all notifications"""
    all_notifications = Notification.objects.filter(
        recipient=request.user
    ).select_related('actor', 'group', 'session')
    
    # Filter by type if specified
    filter_type = request.GET.get('type')
    if filter_type:
        all_notifications = all_notifications.filter(notification_type=filter_type)
    
    # Filter by read status
    filter_status = request.GET.get('status')
    if filter_status == 'unread':
        all_notifications = all_notifications.filter(is_read=False)
    elif filter_status == 'read':
        all_notifications = all_notifications.filter(is_read=True)
    
    context = {
        'notifications': all_notifications,
        'filter_type': filter_type,
        'filter_status': filter_status,
    }
    return render(request, 'notifications/notifications_list.html', context)


@login_required
def mark_as_read(request, notification_id):
    """Mark a notification as read"""
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.mark_as_read()
    
    # Redirect to action URL if exists, otherwise back to notifications
    if notification.action_url:
        return redirect(notification.action_url)
    return redirect('notifications:notifications_list')


@login_required
def mark_all_as_read(request):
    """Mark all notifications as read"""
    from django.utils import timezone
    Notification.objects.filter(
        recipient=request.user,
        is_read=False
    ).update(is_read=True, read_at=timezone.now())
    
    messages.success(request, 'All notifications marked as read.')
    return redirect('notifications:notifications_list')


@login_required
def delete_notification(request, notification_id):
    """Delete a notification"""
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.delete()
    messages.success(request, 'Notification deleted.')
    return redirect('notifications:notifications_list')


@login_required
def notification_preferences(request):
    """Manage notification preferences"""
    prefs, created = NotificationPreference.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Update preferences
        prefs.email_session_reminders = request.POST.get('email_session_reminders') == 'on'
        prefs.email_join_requests = request.POST.get('email_join_requests') == 'on'
        prefs.email_request_responses = request.POST.get('email_request_responses') == 'on'
        prefs.email_new_members = request.POST.get('email_new_members') == 'on'
        prefs.email_session_updates = request.POST.get('email_session_updates') == 'on'
        
        prefs.inapp_session_reminders = request.POST.get('inapp_session_reminders') == 'on'
        prefs.inapp_join_requests = request.POST.get('inapp_join_requests') == 'on'
        prefs.inapp_request_responses = request.POST.get('inapp_request_responses') == 'on'
        prefs.inapp_new_members = request.POST.get('inapp_new_members') == 'on'
        prefs.inapp_session_updates = request.POST.get('inapp_session_updates') == 'on'
        
        prefs.save()
        messages.success(request, 'Notification preferences updated.')
        return redirect('notifications:notification_preferences')
    
    context = {'prefs': prefs}
    return render(request, 'notifications/preferences.html', context)


@login_required
def unread_count_api(request):
    """API endpoint for unread notification count"""
    count = get_unread_count(request.user)
    return JsonResponse({'count': count})