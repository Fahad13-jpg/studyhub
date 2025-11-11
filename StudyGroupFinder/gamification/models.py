from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Badge(models.Model):
    """Achievement badges"""
    BADGE_TYPES = [
        ('founder', 'Group Founder'),
        ('active_member', 'Active Member'),
        ('session_creator', 'Session Creator'),
        ('perfect_attendance', 'Perfect Attendance'),
        ('social_butterfly', 'Social Butterfly'),
        ('early_bird', 'Early Bird'),
        ('night_owl', 'Night Owl'),
        ('streak_master', 'Streak Master'),
        ('veteran', 'Veteran'),
        ('helpful', 'Helpful Member'),
    ]
    
    BADGE_TIERS = [
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('platinum', 'Platinum'),
    ]
    
    name = models.CharField(max_length=100)
    badge_type = models.CharField(max_length=20, choices=BADGE_TYPES)
    tier = models.CharField(max_length=10, choices=BADGE_TIERS)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='fa-trophy')  # FontAwesome icon
    color = models.CharField(max_length=20, default='#667eea')  # Badge color
    
    # Requirements
    requirement_value = models.IntegerField(default=0)
    requirement_description = models.CharField(max_length=200)
    
    points = models.IntegerField(default=10)  # Points awarded
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['badge_type', 'tier']
        unique_together = ['badge_type', 'tier']
    
    def __str__(self):
        return f"{self.name} ({self.tier})"


class UserBadge(models.Model):
    """Badges earned by users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='earned_badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-earned_at']
        unique_together = ['user', 'badge']
    
    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"


class StudyStreak(models.Model):
    """Track study streaks for users"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='study_streak')
    
    current_streak = models.IntegerField(default=0)  # Current consecutive weeks
    longest_streak = models.IntegerField(default=0)  # All-time longest streak
    
    last_activity_date = models.DateField(null=True, blank=True)
    streak_start_date = models.DateField(null=True, blank=True)
    
    total_sessions_attended = models.IntegerField(default=0)
    total_groups_joined = models.IntegerField(default=0)
    total_sessions_created = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Study Streak"
        verbose_name_plural = "Study Streaks"
    
    def __str__(self):
        return f"{self.user.username} - {self.current_streak} week streak"
    
    def update_streak(self):
        """Update streak based on recent activity"""
        from datetime import timedelta
        today = timezone.now().date()
        
        # If no last activity, start fresh
        if not self.last_activity_date:
            self.current_streak = 1
            self.longest_streak = 1
            self.last_activity_date = today
            self.streak_start_date = today
            self.save()
            return
        
        days_since_last = (today - self.last_activity_date).days
        
        # Same week - don't update streak count
        if days_since_last < 7:
            self.last_activity_date = today
            self.save()
            return
        
        # Within next week - increment streak
        if 7 <= days_since_last < 14:
            self.current_streak += 1
            if self.current_streak > self.longest_streak:
                self.longest_streak = self.current_streak
            self.last_activity_date = today
            self.save()
            return
        
        # Streak broken - reset
        self.current_streak = 1
        self.last_activity_date = today
        self.streak_start_date = today
        self.save()


class UserPoints(models.Model):
    """Track user points and level"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='points')
    
    total_points = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    
    # Point breakdown
    points_from_badges = models.IntegerField(default=0)
    points_from_sessions = models.IntegerField(default=0)
    points_from_groups = models.IntegerField(default=0)
    points_from_social = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User Points"
        verbose_name_plural = "User Points"
    
    def __str__(self):
        return f"{self.user.username} - Level {self.level} ({self.total_points} pts)"
    
    def add_points(self, points, category='other'):
        """Add points and update level"""
        self.total_points += points
        
        # Update category points
        if category == 'badges':
            self.points_from_badges += points
        elif category == 'sessions':
            self.points_from_sessions += points
        elif category == 'groups':
            self.points_from_groups += points
        elif category == 'social':
            self.points_from_social += points
        
        # Calculate level (100 points per level)
        self.level = (self.total_points // 100) + 1
        
        self.save()
    
    def points_to_next_level(self):
        """Calculate points needed for next level"""
        next_level_points = self.level * 100
        return next_level_points - self.total_points


class Achievement(models.Model):
    """Special achievements"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, default='fa-star')
    color = models.CharField(max_length=20, default='#ffd700')
    
    # Requirements (flexible JSON field)
    requirement_type = models.CharField(max_length=50)  # e.g., 'sessions_attended', 'groups_created'
    requirement_value = models.IntegerField()
    
    points_reward = models.IntegerField(default=50)
    is_hidden = models.BooleanField(default=False)  # Hidden until earned
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['requirement_value']
    
    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    """Achievements earned by users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)
    progress = models.IntegerField(default=0)  # Track progress towards achievement
    
    class Meta:
        ordering = ['-earned_at']
        unique_together = ['user', 'achievement']
    
    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"