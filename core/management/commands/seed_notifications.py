import random
from django.core.management.base import BaseCommand
from core.models import Notification

TITLES = [
    "New Placement Drive Announced",
    "Interview Schedule Released",
    "Shortlisted Candidates Published",
    "Company Registration Closing Soon",
    "Placement Orientation Session",
    "Mock Interview Training",
]

MESSAGES = [
    "Please check the dashboard for further details.",
    "Ensure you complete the form before the deadline.",
    "Attendance is mandatory for all final-year students.",
    "Slots are allocated on a first-come-first-serve basis.",
    "Bring your updated resume and college ID card.",
]

class Command(BaseCommand):
    help = "Seed mock notifications"

    def handle(self, *args, **kwargs):

        Notification.objects.all().delete()

        notifications = []

        for i in range(30):
            notifications.append(
                Notification(
                    title=random.choice(TITLES),
                    message=random.choice(MESSAGES),
                    pinned=random.choice([True, False]),
                )
            )

        Notification.objects.bulk_create(notifications)
        self.stdout.write(self.style.SUCCESS("✅ Seeded 30 notifications successfully"))
