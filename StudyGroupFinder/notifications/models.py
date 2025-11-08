from django.db import models
from django.contrib.auth.models import User
from groups.models import StudyGroup, JoinRequest
from user_sessions.models import StudySession

class Notification(models.Model):
    """System notifications for users"""
    NOTIFICATION_TYPES = [
        ('session_reminder', 'Session Reminder'),
        ('join_request', 'Join Request'),
        ('request_approved', 'Request Approved'),
        ('request_rejected', 'Request Rejected'),
        ('new_member', 'New Member'),
        ('session_created', 'Session Created'),
        ('session_cancelled', 'Session Cancelled'),
        ('group_update', 'Group Update'),
        ('member_left', 'Member Left'),
    ]
    
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    # Related objects (optional)
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, null=True, blank=True)
    session = models.ForeignKey(StudySession, on_delete=models.CASCADE, null=True, blank=True)
    join_request = models.ForeignKey(JoinRequest, on_delete=models.CASCADE, null=True, blank=True)
    actor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='sent_notifications')
    
    # Notification state
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Links
    action_url = models.CharField(max_length=500, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.notification_type} for {self.recipient.username}"
    
    def mark_as_read(self):
        """Mark notification as read"""
        from django.utils import timezone
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()


class NotificationPreference(models.Model):
    """User preferences for notifications"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preferences')
    
    # Email notifications
    email_session_reminders = models.BooleanField(default=True)
    email_join_requests = models.BooleanField(default=True)
    email_request_responses = models.BooleanField(default=True)
    email_new_members = models.BooleanField(default=False)
    email_session_updates = models.BooleanField(default=True)
    
    # In-app notifications
    inapp_session_reminders = models.BooleanField(default=True)
    inapp_join_requests = models.BooleanField(default=True)
    inapp_request_responses = models.BooleanField(default=True)
    inapp_new_members = models.BooleanField(default=True)
    inapp_session_updates = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Notification preferences for {self.user.username}"