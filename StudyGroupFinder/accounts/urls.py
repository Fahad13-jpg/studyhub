from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication URLs
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Profile URLs
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),  # STATIC route first
    path('profile/', views.profile_view, name='profile'),                 # Current user's profile
    path('profile/<str:username>/', views.profile_view, name='profile_detail'),  # DYNAMIC route last
]
