from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Create default admin users"

    def handle(self, *args, **kwargs):

        admins = [
            ("admin", "admin123"),
            ("placement_head", "placement123"),
        ]

        for username, password in admins:
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(username=username, password=password)
                self.stdout.write(self.style.SUCCESS(f"✅ Admin created: {username}"))

        self.stdout.write(self.style.SUCCESS("✅ Admin seeding complete"))
