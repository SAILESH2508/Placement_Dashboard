from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from companies.models import Company
from placements.models import Job, Application
from notifications.models import Notification
from students.models import Student
import random
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds companies, jobs, applications, and notifications'

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting Company & Placement Data Seeding...")

        # 1. Clear existing data (Optional, good for idempotency if we want a fresh start)
        # Application.objects.all().delete()
        # Job.objects.all().delete()
        # Company.objects.all().delete()
        # Notification.objects.all().delete()
        # self.stdout.write("Cleared existing placement data.")

        # 2. Create 130 Companies
        cities = ["Bangalore", "Hyderabad", "Pune", "Chennai", "Delhi", "Mumbai", "Gurgaon", "Noida"]
        sectors = ["Tech", "Finance", "Consulting", "Health", "Edu", "Auto", "Logistics", "Retail"]
        
        companies_to_create = []
        for i in range(1, 131):
            name = f"{random.choice(sectors)} Solutions {i}"
            if i % 2 == 0: name = f"Global {random.choice(sectors)} {i}"
            if i % 3 == 0: name = f"{random.choice(sectors)} Systems {i}"
            
            companies_to_create.append(Company(
                name=name,
                website=f"https://www.company{i}.com",
                city=random.choice(cities),
                description=f"A leading company in the {random.choice(sectors)} sector.",
                contact_email=f"hr@company{i}.com"
            ))
        
        Company.objects.bulk_create(companies_to_create)
        self.stdout.write(f"Created {len(companies_to_create)} companies.")
        
        # 3. Create Jobs (2 per company)
        all_companies = list(Company.objects.all())
        jobs_to_create = []
        titles = ["Software Engineer", "Data Analyst", "Product Manager", "System Eng", "Sales Exec", "HR Intern", "Marketing Lead"]
        
        for company in all_companies:
            for _ in range(2): # 2 jobs per company
                jobs_to_create.append(Job(
                    company=company,
                    title=random.choice(titles),
                    description=f"We are hiring for {company.name}. Good salary and benefits.",
                    location=company.city,
                    salary=f"{random.randint(4, 25)} LPA",
                    application_deadline=timezone.now() + timedelta(days=random.randint(10, 60))
                ))
        
        Job.objects.bulk_create(jobs_to_create)
        self.stdout.write(f"Created {len(jobs_to_create)} jobs.")

        # 4. Create Applications
        # Link Students to Jobs
        students = list(Student.objects.all())
        jobs = list(Job.objects.all())
        
        if not students:
            self.stdout.write("No students found! Run seed_students first.")
            return

        applications_to_create = []
        # Randomly assign 0-3 applications per student
        for student in students:
            selected_jobs = random.sample(jobs, k=random.randint(0, 3))
            for job in selected_jobs:
                applications_to_create.append(Application(
                    student=student,
                    job=job,
                    status=random.choice(['applied', 'shortlisted', 'applied', 'rejected', 'accepted', 'offered']), # Weighted mix
                    notes="Applied via portal"
                ))
                
        # Bulk create might fail if there are duplicates (unique_together), but random.sample on unique jobs list prevents dupes for same student
        Application.objects.bulk_create(applications_to_create)
        self.stdout.write(f"Created {len(applications_to_create)} applications.")

        # 5. Notifications
        # Create some notifications for random users
        users = list(User.objects.filter(student_profile__isnull=False)[:50]) # First 50 students
        notifications = []
        for user in users:
            notifications.append(Notification(
                user=user,
                title="Welcome to Placement Portal",
                message="Your profile has been successfully created. Start applying for jobs!",
                is_read=False
            ))
            notifications.append(Notification(
                user=user,
                title="New Job Alert",
                message="Check out the new openings in your dashboard.",
                is_read=False
            ))
            
        Notification.objects.bulk_create(notifications)
        self.stdout.write("Created sample notifications.")

        self.stdout.write(self.style.SUCCESS('Seeding Complete!'))
