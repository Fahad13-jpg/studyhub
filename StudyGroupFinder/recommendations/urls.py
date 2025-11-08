from django.urls import path
from . import views

app_name = 'recommendations'

urlpatterns = [
    path('', views.recommendations_page, name='recommendations_page'),
    path('refresh/', views.refresh_recommendations, name='refresh_recommendations'),
]