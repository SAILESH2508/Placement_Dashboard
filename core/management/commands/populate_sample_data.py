"""
Management command to populate the database with sample data for testing
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Student, Company, Placement, Notification
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Populate database with sample data for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--students',
            type=int,
            default=50,
            help='Number of students to create'
        )
        parser.add_argument(
            '--companies',
            type=int,
            default=20,
            help='Number of companies to create'
        )

    def handle(self, *args, **options):
        num_students = options['students']
        num_companies = options['companies']

        self.stdout.write(self.style.SUCCESS('Starting data population...'))

        # Create companies
        self.stdout.write('Creating companies...')
        companies = []
        company_names = [
            'Google', 'Microsoft', 'Amazon', 'Apple', 'Meta',
            'Netflix', 'Tesla', 'IBM', 'Oracle', 'Adobe',
            'Salesforce', 'Intel', 'Cisco', 'SAP', 'VMware',
            'Uber', 'Airbnb', 'Twitter', 'LinkedIn', 'Spotify'
        ]
        
        locations = ['Bangalore', 'Mumbai', 'Hyderabad', 'Pune', 'Delhi', 'Chennai']
        
        for i in range(min(num_companies, len(company_names))):
            company, created = Company.objects.get_or_create(
                name=company_names[i],
                defaults={
                    'description': f'{company_names[i]} is a leading technology company.',
                    'website': f'https://www.{company_names[i].lower()}.com',
                    'location': random.choice(locations),
                    'recruiter_contact': f'recruiter@{company_names[i].lower()}.com'
                }
            )
            companies.append(company)
            if created:
                self.stdout.write(f'  Created: {company.name}')

        # Create students
        self.stdout.write('Creating students...')
        branches = ['CSE', 'ECE', 'EEE', 'MECH', 'CIVIL', 'IT']
        students = []
        
        for i in range(num_students):
            # Create user
            username = f'student{i+1}'
            email = f'student{i+1}@college.edu'
            
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': f'Student{i+1}',
                    'last_name': 'Test'
                }
            )
            
            if created:
                user.set_password('password123')
                user.save()
            
            # Create student
            roll_no = f'2021{random.choice(branches)}{str(i+1).zfill(3)}'
            student, created = Student.objects.get_or_create(
                roll_no=roll_no,
                defaults={
                    'user': user,
                    'branch': random.choice(branches),
                    'year': random.randint(3, 4),
                    'cgpa': round(random.uniform(6.0, 9.5), 2),
                    'resume_link': f'https://example.com/resume/{roll_no}.pdf'
                }
            )
            students.append(student)
            
            if created:
                self.stdout.write(f'  Created: {student.roll_no}')

        # Create placements
        self.stdout.write('Creating placements...')
        placement_count = 0
        
        # Place about 60% of students
        num_placements = int(num_students * 0.6)
        selected_students = random.sample(students, num_placements)
        
        for student in selected_students:
            # Some students get multiple offers
            num_offers = random.choices([1, 2, 3], weights=[70, 25, 5])[0]
            
            for _ in range(num_offers):
                company = random.choice(companies)
                
                # Check if placement already exists
                if Placement.objects.filter(student=student, company=company).exists():
                    continue
                
                placement = Placement.objects.create(
                    student=student,
                    company=company,
                    position=random.choice([
                        'Software Engineer',
                        'Data Analyst',
                        'Product Manager',
                        'DevOps Engineer',
                        'Full Stack Developer'
                    ]),
                    package_lpa=round(random.uniform(6.0, 25.0), 2),
                    date_offered=date.today() - timedelta(days=random.randint(0, 180)),
                    confirmed=random.choice([True, False])
                )
                placement_count += 1

        self.stdout.write(f'  Created: {placement_count} placements')

        # Create notifications
        self.stdout.write('Creating notifications...')
        notifications = [
            {
                'title': 'Welcome to Placement Portal',
                'message': 'Welcome to the placement management system. Stay updated with latest opportunities.',
                'pinned': True
            },
            {
                'title': 'Google Drive Scheduled',
                'message': 'Google campus drive scheduled for next week. Eligible students please register.',
                'pinned': True
            },
            {
                'title': 'Resume Workshop',
                'message': 'Resume building workshop on Friday at 3 PM in Auditorium.',
                'pinned': False
            },
            {
                'title': 'Mock Interview Sessions',
                'message': 'Mock interview sessions will be conducted from Monday. Register now!',
                'pinned': False
            },
        ]
        
        for notif_data in notifications:
            notif, created = Notification.objects.get_or_create(
                title=notif_data['title'],
                defaults={
                    'message': notif_data['message'],
                    'pinned': notif_data['pinned']
                }
            )
            if created:
                self.stdout.write(f'  Created: {notif.title}')

        # Summary
        self.stdout.write(self.style.SUCCESS('\n' + '='*60))
        self.stdout.write(self.style.SUCCESS('Data population complete!'))
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(f'Companies: {len(companies)}')
        self.stdout.write(f'Students: {len(students)}')
        self.stdout.write(f'Placements: {placement_count}')
        self.stdout.write(f'Notifications: {len(notifications)}')
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write('\nDefault credentials for students:')
        self.stdout.write('  Username: student1, student2, ...')
        self.stdout.write('  Password: password123')
