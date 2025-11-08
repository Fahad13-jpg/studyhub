from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from user_sessions.models import StudySession
from notifications.utils import notify_session_reminder

class Command(BaseCommand):
    help = 'Send reminders for sessions happening in 24 hours'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        tomorrow = now + timedelta(hours=24)
        
        # Get sessions happening in next 24 hours
        upcoming_sessions = StudySession.objects.filter(
            date=tomorrow.date(),
            is_cancelled=False
        )
        
        count = 0
        for session in upcoming_sessions:
            notify_session_reminder(session)
            count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully sent {count} session reminders')
        )