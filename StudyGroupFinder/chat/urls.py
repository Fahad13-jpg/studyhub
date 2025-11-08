from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('group/<int:group_id>/', views.group_chat, name='group_chat'),
    path('message/<int:message_id>/delete/', views.delete_message, name='delete_message'),
    path('message/<int:message_id>/edit/', views.edit_message, name='edit_message'),
    path('api/unread/<int:group_id>/', views.get_unread_count, name='unread_count'),
]