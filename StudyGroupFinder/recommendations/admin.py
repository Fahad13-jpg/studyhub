from django.contrib import admin
from .models import SearchHistory, GroupView, RecommendationScore

@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'query', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'query']
    date_hierarchy = 'created_at'

@admin.register(GroupView)
class GroupViewAdmin(admin.ModelAdmin):
    list_display = ['user', 'group', 'viewed_at']
    list_filter = ['viewed_at']
    search_fields = ['user__username', 'group__name']
    date_hierarchy = 'viewed_at'

@admin.register(RecommendationScore)
class RecommendationScoreAdmin(admin.ModelAdmin):
    list_display = ['user', 'group', 'score', 'updated_at']
    list_filter = ['updated_at']
    search_fields = ['user__username', 'group__name']
    readonly_fields = ['created_at', 'updated_at']