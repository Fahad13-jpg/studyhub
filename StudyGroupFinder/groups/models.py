from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class StudyGroup(models.Model):
    """Study group for courses with members"""
    DAYS_CHOICES = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]
    
    GROUP_TYPE_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]
    
    name = models.CharField(max_length=200)
    course_name = models.CharField(max_length=200)
    course_code = models.CharField(max_length=50)
    description = models.TextField()
    study_topics = models.TextField(help_text="Topics covered in this group")
    max_capacity = models.IntegerField(
        validators=[MinValueValidator(3), MaxValueValidator(10)],
        default=5
    )
    meeting_days = models.CharField(max_length=100, help_text="e.g., Monday, Wednesday")
    meeting_time = models.TimeField()
    meeting_location = models.CharField(max_length=200)
    group_type = models.CharField(max_length=10, choices=GROUP_TYPE_CHOICES, default='public')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_groups')
    members = models.ManyToManyField(User, through='GroupMember', related_name='joined_groups')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.course_code}"
    
    def current_member_count(self):
        return self.members.count()
    
    def is_full(self):
        return self.current_member_count() >= self.max_capacity
    
    def can_join(self, user):
        return not self.is_full() and user not in self.members.all()


class GroupMember(models.Model):
    """Through model for group membership"""
    ROLE_CHOICES = [
        ('creator', 'Creator'),
        ('member', 'Member'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'group']
    
    def __str__(self):
        return f"{self.user.username} in {self.group.name}"


class JoinRequest(models.Model):
    """Join requests for private groups"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'group']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} -> {self.group.name}"