from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('group/<int:group_id>/', views.group_analytics, name='group_analytics'),
    path('group/<int:group_id>/refresh/', views.refresh_analytics, name='refresh_analytics'),
]