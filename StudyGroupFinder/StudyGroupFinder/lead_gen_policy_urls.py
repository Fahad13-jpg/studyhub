"""Public informational pages; no login, customer data lookup or database write."""
from django.urls import path
from django.views.generic import TemplateView

class WhatsAppSetupView(TemplateView):
    """Public status only; never launches SDK or accepts onboarding credentials."""
    template_name = 'lead_gen/whatsapp_connect.html'
    http_method_names = ['get', 'head', 'options']

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)
        response['Cache-Control'] = 'no-store'
        response['Referrer-Policy'] = 'no-referrer'
        response['X-Content-Type-Options'] = 'nosniff'
        response['Content-Security-Policy'] = "default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'"
        return response

app_name = 'lead_gen_policies'
urlpatterns = [
    path('whatsapp/connect/', WhatsAppSetupView.as_view(), name='whatsapp_connect'),
    path('privacy/', TemplateView.as_view(template_name='lead_gen/privacy.html'), name='privacy'),
    path('data-deletion/', TemplateView.as_view(template_name='lead_gen/data_deletion.html'), name='data_deletion'),
]
