from django.db import models
from django.contrib.auth.models import User
from groups.models import StudyGroup


class SearchHistory(models.Model):
    """Track user search queries for recommendations"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_history')
    query = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Search Histories"

    def __str__(self):
        return f"{self.user.username} searched: {self.query}"


class GroupView(models.Model):
    """Track which groups users have viewed"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='viewed_groups')
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE, related_name='views')
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-viewed_at']

    def __str__(self):
        return f"{self.user.username} viewed {self.group.name}"


class RecommendationScore(models.Model):
    """Cache recommendation scores for performance"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    group = models.ForeignKey(StudyGroup, on_delete=models.CASCADE)
    score = models.FloatField(default=0.0)
    reasons = models.JSONField(default=list)  # List of reasons for recommendation
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'group']
        ordering = ['-score', '-updated_at']

    def __str__(self):
        return f"{self.group.name} for {self.user.username}: {self.score}"
