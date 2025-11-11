from django.urls import path
from . import views

app_name = 'gamification'

urlpatterns = [
    path('achievements/', views.achievements_page, name='achievements'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]