import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from core.models import Placement, Student, Company

POSITIONS = [
    "Software Engineer", "Associate Developer", "Data Analyst", "AI Engineer",
    "Machine Learning Intern", "QA Engineer", "Cloud Associate",
    "Security Analyst", "Backend Developer", "Full Stack Engineer"
]

class Command(BaseCommand):
    help = "Seed 500 placement offers"

    def handle(self, *args, **kwargs):

        Placement.objects.all().delete()

        students = list(Student.objects.all())
        companies = list(Company.objects.all())

        if len(students) == 0:
            self.stdout.write(self.style.ERROR("❌ No students found! Run seed_data first."))
            return

        if len(companies) == 0:
            self.stdout.write(self.style.ERROR("❌ No companies found! Run seed_companies first."))
            return

        placements = []

        for _ in range(500):
            student = random.choice(students)
            company = random.choice(companies)
            position = random.choice(POSITIONS)
            package = round(random.uniform(3.0, 25.0), 2)  # LPA
            date_offered = date.today() - timedelta(days=random.randint(1, 300))
            confirmed = random.choice([True, False])

            placements.append(
                Placement(
                    student=student,
                    company=company,
                    position=position,
                    package_lpa=package,
                    date_offered=date_offered,
                    confirmed=confirmed
                )
            )

        Placement.objects.bulk_create(placements)
        self.stdout.write(self.style.SUCCESS("✅ Successfully created 500 placement offers!"))
