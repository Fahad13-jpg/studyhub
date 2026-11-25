"""Regression checks for the Folio Commons presentation and restored settings UI."""
from datetime import date, time, timedelta
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse
from groups.models import StudyGroup, GroupMember
from user_sessions.models import StudySession
from notifications.models import NotificationPreference
from django.conf import settings
import glob
import json
from pathlib import Path


@override_settings(DEBUG=True, DEFAULT_FILE_STORAGE='django.core.files.storage.FileSystemStorage', PASSWORD_HASHERS=['django.contrib.auth.hashers.MD5PasswordHasher'])
class DesignScreensTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.student = User.objects.create_user('design-student', password='TestOnly!284', first_name='Mina')
        cls.peer = User.objects.create_user('design-peer')
        cls.group = StudyGroup.objects.create(name='A study circle', course_name='Calculus', course_code='MATH 201', description='A shared learning space.', study_topics='Integration', creator=cls.student, max_capacity=6, meeting_days='Wednesday', meeting_time=time(16, 0), meeting_location='Library')
        GroupMember.objects.create(user=cls.student, group=cls.group, role='creator')
        GroupMember.objects.create(user=cls.peer, group=cls.group)
        cls.session = StudySession.objects.create(group=cls.group, title='Practice together', description='Questions and practice.', date=date.today() + timedelta(days=1), time=time(16, 0), duration=60, location='Library', created_by=cls.student)

    def setUp(self):
        self.client.force_login(self.student)

    def test_public_entry_screens_render(self):
        self.client.logout()
        for name in ['home', 'accounts:login', 'accounts:register']:
            with self.subTest(screen=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, 'Folio Commons')

    def test_all_application_screens_render(self):
        targets = [('dashboard:dashboard', {}), ('groups:browse_groups', {}), ('groups:my_groups', {}), ('groups:create_group', {}), ('groups:group_detail', {'pk': self.group.pk}), ('user_sessions:group_sessions', {'group_id': self.group.pk}), ('user_sessions:create_session', {'group_id': self.group.pk}), ('user_sessions:session_detail', {'pk': self.session.pk}), ('chat:group_chat', {'group_id': self.group.pk}), ('recommendations:recommendations_page', {}), ('notifications:notifications_list', {}), ('notifications:notification_preferences', {}), ('accounts:profile', {}), ('accounts:edit_profile', {}), ('gamification:achievements', {}), ('gamification:leaderboard', {}), ('analytics:group_analytics', {'group_id': self.group.pk})]
        for name, kwargs in targets:
            with self.subTest(screen=name):
                response = self.client.get(reverse(name, kwargs=kwargs))
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, 'Folio Commons')
                self.assertNotContains(response, '{{')

    def test_dashboard_member_count_includes_other_members(self):
        self.client.force_login(self.peer)
        response = self.client.get(reverse('dashboard:dashboard'))
        self.assertEqual(list(response.context['joined_groups'])[0].member_total, 2)
        self.assertEqual(response.content.decode().count('btn btn-primary'), 1)

    def test_group_and_session_forms_render_validation(self):
        for name, kwargs in [('groups:create_group', {}), ('user_sessions:create_session', {'group_id': self.group.pk})]:
            with self.subTest(form=name):
                response = self.client.post(reverse(name, kwargs=kwargs), {})
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, 'This field is required.')

    def test_preferences_controls_and_save(self):
        response = self.client.get(reverse('notifications:notification_preferences'))
        self.assertEqual(response.content.decode().count('type="checkbox"'), 10)
        response = self.client.post(reverse('notifications:notification_preferences'), {'email_session_reminders': 'on', 'inapp_session_updates': 'on'})
        self.assertEqual(response.status_code, 302)
        prefs = NotificationPreference.objects.get(user=self.student)
        self.assertTrue(prefs.email_session_reminders)
        self.assertTrue(prefs.inapp_session_updates)
        self.assertFalse(prefs.email_new_members)

    def test_vercel_includes_application_static_assets(self):
        config = json.loads((settings.BASE_DIR / 'vercel.json').read_text())
        published = set()
        for builder in config['builds']:
            if builder['use'] == '@vercel/static':
                published.update(Path(path).resolve() for path in glob.glob(str(settings.BASE_DIR / builder['src']), recursive=True))
        for asset in ['home.css', 'folio.css', 'workspace.css', 'auth.css', 'slider.js', 'mark.svg', 'study-table.webp', 'manrope.ttf']:
            with self.subTest(asset=asset):
                self.assertIn((settings.BASE_DIR / 'static' / 'folio' / asset).resolve(), published)
