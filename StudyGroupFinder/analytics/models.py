from django.db import models
from django.contrib.auth.models import User
from groups.models import StudyGroup
from user_sessions.models import StudySession

class GroupAnalytics(models.Model):
    """Cached analytics data for groups"""
    group = models.OneToOneField(StudyGroup, on_delete=models.CASCADE, related_name='analytics')
    
    # Member statistics
    total_members = models.IntegerField(default=0)
    member_growth_rate = models.FloatField(default=0.0)  # Percentage
    
    # Session statistics
    total_sessions = models.IntegerField(default=0)
    completed_sessions = models.IntegerField(default=0)
    cancelled_sessions = models.IntegerField(default=0)
    average_attendance_rate = models.FloatField(default=0.0)  # Percentage
    
    # Activity statistics
    most_active_member = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    most_active_member_score = models.IntegerField(default=0)
    
    # Time-based statistics
    sessions_this_month = models.IntegerField(default=0)
    sessions_last_month = models.IntegerField(default=0)
    
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Group Analytics"
        verbose_name_plural = "Group Analytics"
    
    def __str__(self):
        return f"Analytics for {self.group.name}"


class MemberActivity(models.Model):
    """Track individual member activity in groups"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)
    
    # Activity metrics
    sessions_attended = models.IntegerField(default=0)
    sessions_created = models.IntegerField(default=0)
    messages_sent = models.IntegerField(default=0)
    
    # Engagement score (calculated)
    activity_score = models.IntegerField(default=0)
    
    last_activity = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'group']
        ordering = ['-activity_score']
    
    def __str__(self):
        return f"{self.user.username} in {self.group.name}"
    
    def calculate_activity_score(self):
        """Calculate activity score based on metrics"""
        score = (
            self.sessions_attended * 10 +
            self.sessions_created * 15 +
            self.messages_sent * 2
        )
        self.activity_score = score
        self.save()
        return score


class SessionAttendanceLog(models.Model):
    """Log attendance for analytics"""
    session = models.ForeignKey(StudySession, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attended = models.BooleanField(default=False)
    logged_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['session', 'user']
    
    def __str__(self):
        return f"{self.user.username} - {self.session.title}"