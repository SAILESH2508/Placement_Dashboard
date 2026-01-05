from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from students.models import Student
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds the database with 1140 students across 13 departments'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Seeding data... This may take a moment.'))

        # Department Config
        # Format: (Name, Count, Code)
        departments = [
            ("CSE", 180, "CS"),
            ("IT", 120, "IT"),
            ("AIML", 120, "AI"),
            ("AIDS", 120, "AD"),
            ("Cyber", 120, "CY"),
            ("Mech", 60, "ME"),
            ("Civil", 60, "CE"),
            ("EEE", 60, "EE"),
            ("ECE", 60, "EC"),
            ("FoodTech", 60, "FT"),
            ("Agri", 60, "AG"),
            ("Biomedical", 60, "BM"),
            ("Biotech", 60, "BT"),
        ]

        total_created = 0
        
        # Optional: Clear existing students? 
        # For now, let's just append or skip if exists to avoid unique constraint errors
        # logic: try create, if roll no exists, skip.

        for dept_name, count, dept_code in departments:
            self.stdout.write(f"Processing {dept_name} ({count} students)...")
            
            for i in range(1, count + 1):
                # Roll No: 23 + Code + 3-digit number (e.g., 23CS001)
                roll_no = f"23{dept_code}{i:03d}"
                username = roll_no
                email = f"{roll_no.lower()}@college.edu"
                password = "pass123" # Default password

                if User.objects.filter(username=username).exists():
                    continue

                # Create User
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    role='student', # Custom User model field
                    first_name=f"Student",
                    last_name=f"{roll_no}"
                )

                # Create Student Profile
                Student.objects.create(
                    user=user,
                    roll_no=roll_no,
                    course=dept_name,
                    year=3, # Assuming 3rd year for '23' batch in 2025 context or generic
                    cgpa=round(random.uniform(6.0, 9.8), 2),
                    phone=f"98{random.randint(10000000, 99999999)}"
                )
                total_created += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {total_created} students.'))
