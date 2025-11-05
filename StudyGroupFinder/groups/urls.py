from django.urls import path
from . import views

app_name = 'groups'

urlpatterns = [
    path('create/', views.create_group, name='create_group'),
    path('browse/', views.browse_groups, name='browse_groups'),
    path('my-groups/', views.my_groups, name='my_groups'),
    path('<int:pk>/', views.group_detail, name='group_detail'),
    path('<int:pk>/join/', views.join_group, name='join_group'),
    path('<int:pk>/leave/', views.leave_group, name='leave_group'),
    path('<int:pk>/delete/', views.delete_group, name='delete_group'),
    path('request/<int:request_id>/approve/', views.approve_request, name='approve_request'),
    path('request/<int:request_id>/reject/', views.reject_request, name='reject_request'),
]