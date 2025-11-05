from django.db import models
from django.contrib.auth.models import User
from groups.models import StudyGroup
from django.utils import timezone

class StudySession(models.Model):
    """Study session for a group"""
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name='sessions')
    title = models.CharField(max_length=200)
    description = models.TextField(help_text="Agenda or session description")
    date = models.DateField()
    time = models.TimeField()
    duration = models.IntegerField(help_text="Duration in minutes")
    location = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_sessions')
    is_cancelled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['date', 'time']
    
    def __str__(self):
        return f"{self.title} - {self.date}"
    
    def is_upcoming(self):
        from datetime import datetime
        session_datetime = datetime.combine(self.date, self.time)
        return session_datetime > datetime.now() and not self.is_cancelled
    
    def attending_count(self):
        return self.rsvps.filter(status='attending').count()
    
    def maybe_count(self):
        return self.rsvps.filter(status='maybe').count()
    
    def cannot_count(self):
        return self.rsvps.filter(status='cannot').count()


class SessionRSVP(models.Model):
    """RSVP for study sessions"""
    STATUS_CHOICES = [
        ('attending', 'Attending'),
        ('maybe', 'Maybe'),
        ('cannot', 'Cannot Attend'),
    ]
    
    session = models.ForeignKey(StudySession, on_delete=models.CASCADE, related_name='rsvps')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='attending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['session', 'user']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.session.title} ({self.status})"