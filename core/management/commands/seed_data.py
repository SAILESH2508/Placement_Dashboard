# core/management/commands/seed_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction, connection
from django.contrib.auth.hashers import make_password

from faker import Faker
from datetime import datetime, timedelta
import random

from core.models import Student, Company, Placement, PlacementStatistic

fake = Faker()

# 13 branches
BRANCHES = [
    "CSE", "IT", "ECE", "EEE", "MECH", "CIVIL",
    "AIML", "DS", "BT", "CHE", "AUTO", "FT", "AGRI"
]

# Two-letter codes for roll numbers
BRANCH_CODE = {
    "CSE": "CS",
    "IT": "IT",
    "ECE": "EC",
    "EEE": "EE",
    "MECH": "ME",
    "CIVIL": "CE",
    "AIML": "AM",
    "DS": "DS",
    "BT": "BT",
    "CHE": "CH",
    "AUTO": "AU",
    "FT": "FT",
    "AGRI": "AG",
}

def make_roll_no(year_prefix_2digit: int, branch: str, seq: int) -> str:
    """
    Return roll number like '23CS0109'
    year_prefix_2digit -> 23
    branch -> 'CSE' -> 'CS'
    seq -> zero-padded 4 digits
    """
    return f"{year_prefix_2digit:02d}{BRANCH_CODE.get(branch, 'XX')}{seq:04d}"

class Command(BaseCommand):
    help = "Seed fast: 2000 students, 100 companies, 500 placements, 30 daily stats."

    def handle(self, *args, **kwargs):
        # 1) Apply SQLite PRAGMAs OUTSIDE a transaction
        if connection.vendor == "sqlite":
            with connection.cursor() as cur:
                cur.execute("PRAGMA journal_mode=WAL;")
                cur.execute("PRAGMA synchronous = NORMAL;")
                cur.execute("PRAGMA temp_store = MEMORY;")

        TOTAL_STUDENTS = 2000
        TOTAL_COMPANIES = 100
        TOTAL_PLACEMENTS = 500

        self.stdout.write(self.style.WARNING("🧹 Cleaning previous seeded data (student_**** users only)…"))

        # 2) All data writes inside ONE atomic block
        with transaction.atomic():
            # Clean previously seeded users & related students (keep admins and other users)
            seeded_users = User.objects.filter(username__startswith="student_")
            Student.objects.filter(user__in=seeded_users).delete()
            seeded_users.delete()

            # Clean other seeded entities
            Placement.objects.all().delete()
            Company.objects.all().delete()
            PlacementStatistic.objects.all().delete()

            self.stdout.write(self.style.SUCCESS("✅ Cleaned previous seeds (kept admin users)."))

            # ---------- USERS (bulk, pre-hashed password) ----------
            self.stdout.write(self.style.WARNING(f"👤 Creating {TOTAL_STUDENTS} users (bulk)…"))
            hashed_password = make_password("password123")

            user_objs = []
            for i in range(1, TOTAL_STUDENTS + 1):
                uname = f"student_{i:04d}"
                user_objs.append(
                    User(
                        username=uname,
                        email=f"{uname}@example.com",
                        password=hashed_password,  # pre-hashed once
                        first_name=fake.first_name(),
                        last_name=fake.last_name(),
                        is_active=True,
                    )
                )
            User.objects.bulk_create(user_objs, batch_size=500)

            # Re-fetch to ensure PKs populated and in stable order
            users = list(User.objects.filter(username__startswith="student_").order_by("username"))
            self.stdout.write(self.style.SUCCESS("✅ Users created."))

            # ---------- STUDENTS (bulk) ----------
            self.stdout.write(self.style.WARNING("🎓 Creating Students (bulk)…"))
            ADM_YEARS = [21, 22, 23]        # 2021/22/23 -> '21','22','23'
            ACADEMIC_YEARS = [1, 2, 3, 4]   # 1st..4th year

            # Track per-branch sequence to avoid duplicate roll nos
            per_branch_seq = {b: 1 for b in BRANCHES}

            student_objs = []
            for u in users:
                branch = random.choice(BRANCHES)
                yr_prefix = random.choice(ADM_YEARS)
                seq = per_branch_seq[branch]
                per_branch_seq[branch] = seq + 1

                roll_no = make_roll_no(yr_prefix, branch, seq)

                student_objs.append(
                    Student(
                        user=u,
                        roll_no=roll_no,
                        branch=branch,
                        year=random.choice(ACADEMIC_YEARS),
                        cgpa=round(random.uniform(6.0, 9.8), 2),
                        resume_link=f"https://drive.google.com/resume/{u.username}",
                    )
                )

            Student.objects.bulk_create(student_objs, batch_size=500)
            students = list(Student.objects.select_related("user").all())
            self.stdout.write(self.style.SUCCESS("✅ Students created."))

            # ---------- COMPANIES (bulk) ----------
            self.stdout.write(self.style.WARNING(f"🏢 Creating {TOTAL_COMPANIES} companies (bulk)…"))
            company_objs = []
            for _ in range(TOTAL_COMPANIES):
                company_objs.append(
                    Company(
                        name=fake.company(),
                        description=fake.text(max_nb_chars=220),
                        website=fake.url(),
                        location=fake.city(),
                        recruiter_contact=fake.phone_number(),
                    )
                )
            Company.objects.bulk_create(company_objs, batch_size=200)
            companies = list(Company.objects.all())
            self.stdout.write(self.style.SUCCESS("✅ Companies created."))

            # ---------- PLACEMENTS (bulk) ----------
            self.stdout.write(self.style.WARNING(f"📄 Creating {TOTAL_PLACEMENTS} placements (bulk)…"))
            positions = [
                "Software Engineer", "Data Analyst", "ML Engineer", "QA Engineer",
                "DevOps Engineer", "Frontend Developer", "Backend Developer",
                "Cloud Engineer", "Database Engineer", "Business Analyst",
            ]
            today = datetime.now().date()
            placement_objs = []
            # Use a set to reduce accidental duplicate (student, company, position, date) combos
            seen = set()

            for _ in range(TOTAL_PLACEMENTS):
                # keep drawing until unique-ish combo (very low collision chance)
                while True:
                    st = random.choice(students)
                    co = random.choice(companies)
                    pos = random.choice(positions)
                    offered = today - timedelta(days=random.randint(0, 365))
                    key = (st.id, co.id, pos, offered)
                    if key not in seen:
                        seen.add(key)
                        break

                placement_objs.append(
                    Placement(
                        student=st,
                        company=co,
                        position=pos,
                        package_lpa=round(random.uniform(3.0, 28.0), 2),
                        date_offered=offered,
                        confirmed=random.choices([True, False], weights=[70, 30])[0],
                    )
                )

            Placement.objects.bulk_create(placement_objs, batch_size=500)
            self.stdout.write(self.style.SUCCESS("✅ Placements created."))

            # ---------- PLACEMENT STATISTICS (bulk) ----------
            self.stdout.write(self.style.WARNING("📈 Creating PlacementStatistic for last 30 days (bulk)…"))
            stats_objs = []
            for i in range(30):
                d = today - timedelta(days=i)
                stats_objs.append(
                    PlacementStatistic(
                        date=d,
                        total_placed=random.randint(5, 35),
                        average_package_lpa=round(random.uniform(3.5, 16.0), 2),
                    )
                )
            PlacementStatistic.objects.bulk_create(stats_objs, batch_size=200)
            self.stdout.write(self.style.SUCCESS("✅ PlacementStatistic created."))

        self.stdout.write(self.style.SUCCESS("🎉 Seeding complete."))
