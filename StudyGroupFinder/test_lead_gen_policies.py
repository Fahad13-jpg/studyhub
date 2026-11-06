"""Isolated public-page checks: python test_lead_gen_policies.py (no database)."""
from pathlib import Path
import unittest
from django.conf import settings

settings.configure(SECRET_KEY='policy-test-only', ROOT_URLCONF=__name__, ALLOWED_HOSTS=['testserver'], TEMPLATES=[{'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [Path(__file__).parent / 'templates']}])
import django
django.setup()
from django.urls import include, path
from django.test import SimpleTestCase

urlpatterns = [path('lead-gen/', include('StudyGroupFinder.lead_gen_policy_urls'))]

class PolicyTests(SimpleTestCase):
    def test_whatsapp_setup_cannot_launch_or_accept_credentials(self):
        response = self.client.get('/lead-gen/whatsapp/connect/?code=DO_NOT_DISPLAY')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Workspace sign-in is required')
        self.assertContains(response, 'disabled aria-describedby="connection-help"')
        self.assertNotContains(response, '<script')
        self.assertNotContains(response, '<form')
        self.assertNotContains(response, 'DO_NOT_DISPLAY')
        self.assertEqual(response['Cache-Control'], 'no-store')
        self.assertEqual(response['Referrer-Policy'], 'no-referrer')
        self.assertIn("form-action 'none'", response['Content-Security-Policy'])
        self.assertEqual(self.client.post('/lead-gen/whatsapp/connect/', {'code': 'DO_NOT_ACCEPT'}).status_code, 405)

    def test_public_pages_and_cross_links(self):
        for route, other in [('privacy', 'data-deletion'), ('data-deletion', 'privacy')]:
            response = self.client.get(f'/lead-gen/{route}/')
            self.assertEqual(response.status_code, 200)
            self.assertNotIn('Location', response)
            self.assertContains(response, 'Lead-Gen-system')
            self.assertContains(response, f'/lead-gen/{other}/')
            self.assertContains(response, 'mohmmadfahad53408@gmail.com')
            self.assertContains(response, 'temporarily hosted on the StudyHub')

if __name__ == '__main__':
    unittest.main()
