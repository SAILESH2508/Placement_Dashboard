import random
from django.core.management.base import BaseCommand
from core.models import Company

COMPANY_NAMES = [
    "Google", "Amazon", "Microsoft", "Infosys", "TCS", "Wipro",
    "Accenture", "HCL", "Oracle", "Zoho", "IBM", "Deloitte",
    "Cognizant", "Capgemini", "EY", "PwC", "KPMG", "Tech Mahindra",
    "HPE", "Dell", "Adobe", "Samsung", "Nokia", "Siemens",
    "L&T Infotech", "Mindtree", "Byju's", "PhonePe", "Swiggy", "Zomato",
]

LOCATIONS = [
    "Bangalore", "Chennai", "Hyderabad", "Pune", "Mumbai", "Delhi", "Coimbatore"
]

POSITIONS = [
    "Software Engineer", "Data Analyst", "Data Scientist", "Cloud Engineer",
    "Backend Developer", "Frontend Developer", "AI Engineer", "ML Engineer",
    "Testing Engineer", "DevOps Engineer", "Network Engineer"
]

class Command(BaseCommand):
    help = "Seed 100 mock companies"

    def handle(self, *args, **kwargs):

        Company.objects.all().delete()

        companies = []

        for i in range(100):
            name = random.choice(COMPANY_NAMES) + f" Labs {i}"
            companies.append(
                Company(
                    name=name,
                    description="A top-tier company hiring engineering graduates.",
                    website=f"https://www.{name.replace(' ', '').lower()}.com",
                    location=random.choice(LOCATIONS),
                    recruiter_contact=f"hr{i}@{name.replace(' ','').lower()}.com"
                )
            )

        Company.objects.bulk_create(companies)
        self.stdout.write(self.style.SUCCESS("✅ Successfully created 100 mock companies!"))
