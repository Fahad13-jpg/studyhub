"""Public informational pages; no login, customer data lookup or database write."""
from django.urls import path
from django.views.generic import TemplateView

app_name = 'lead_gen_policies'
urlpatterns = [
    path('privacy/', TemplateView.as_view(template_name='lead_gen/privacy.html'), name='privacy'),
    path('data-deletion/', TemplateView.as_view(template_name='lead_gen/data_deletion.html'), name='data_deletion'),
]
