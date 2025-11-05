from django.urls import path
from . import views

app_name = 'user_sessions'

urlpatterns = [
    path('group/<int:group_id>/create/', views.create_session, name='create_session'),
    path('<int:pk>/', views.session_detail, name='session_detail'),
    path('<int:pk>/rsvp/<str:status>/', views.rsvp_session, name='rsvp_session'),
    path('group/<int:group_id>/', views.group_sessions, name='group_sessions'),
    path('<int:pk>/cancel/', views.cancel_session, name='cancel_session'),
    path('<int:pk>/delete/', views.delete_session, name='delete_session'),
]