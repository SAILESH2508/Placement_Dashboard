from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from students.models import Student
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Seeds database students FAST using bulk_create'

    def handle(self, *args, **kwargs):
        self.stdout.write("Preparing data...")
        
        # 1. Cleanup existing non-admin users/students
        Student.objects.all().delete()
        User.objects.filter(is_superuser=False, is_staff=False).delete()
        self.stdout.write("Cleaned partial data.")

        # 2. Pre-compute hash
        password_hash = make_password("pass123")

        departments = [
            ("CSE", 180, "CS"), ("IT", 120, "IT"), ("AIML", 120, "AI"),
            ("AIDS", 120, "AD"), ("Cyber", 120, "CY"), ("Mech", 60, "ME"),
            ("Civil", 60, "CE"), ("EEE", 60, "EE"), ("ECE", 60, "EC"),
            ("FoodTech", 60, "FT"), ("Agri", 60, "AG"), ("Biomedical", 60, "BM"),
            ("Biotech", 60, "BT"),
        ]

        users_to_create = []
        students_to_create = []
        user_id_start = User.objects.order_by('-id').first().id + 1 if User.objects.exists() else 1

        print(f"Starting User ID buffer from: {user_id_start}")
        
        current_id = user_id_start
        for dept_name, count, dept_code in departments:
            for i in range(1, count + 1):
                roll_no = f"23{dept_code}{i:03d}"
                username = roll_no
                email = f"{roll_no.lower()}@college.edu"
                
                # Create User instance
                user = User(
                    id=current_id,
                    username=username,
                    email=email,
                    password=password_hash,
                    role='student',
                    first_name="Student",
                    last_name=roll_no,
                    is_active=True
                )
                users_to_create.append(user)

                # Create Student instance
                student = Student(
                    user_id=current_id, # Link directly via ID
                    roll_no=roll_no,
                    course=dept_name,
                    year=3,
                    cgpa=round(random.uniform(6.0, 9.8), 2),
                    phone=f"98{random.randint(10000000, 99999999)}"
                )
                students_to_create.append(student)
                
                current_id += 1

        # 3. Bulk Create
        self.stdout.write(f"Bulk creating {len(users_to_create)} users...")
        User.objects.bulk_create(users_to_create, batch_size=500)
        
        self.stdout.write(f"Bulk creating {len(students_to_create)} students...")
        Student.objects.bulk_create(students_to_create, batch_size=500)

        self.stdout.write(self.style.SUCCESS(f"Done! Created {len(students_to_create)} records."))
