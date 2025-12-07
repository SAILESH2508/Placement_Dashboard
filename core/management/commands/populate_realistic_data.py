from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Student, Company, Placement
from datetime import date, timedelta
import random

class Command(BaseCommand):
    help = 'Populate database with realistic student data across 13 departments'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting realistic data population...')
        
        # Department configuration
        departments = {
            'CSE': {'count': 180, 'code': 'CS'},
            'IT': {'count': 120, 'code': 'IT'},
            'CSE(CS)': {'count': 120, 'code': 'CC'},
            'AIML': {'count': 120, 'code': 'AI'},
            'AIDS': {'count': 120, 'code': 'AD'},
            'Food Tech': {'count': 60, 'code': 'FT'},
            'Mech': {'count': 60, 'code': 'ME'},
            'EEE': {'count': 60, 'code': 'EE'},
            'ECE': {'count': 60, 'code': 'EC'},
            'Agri': {'count': 60, 'code': 'AG'},
            'Bio Tech': {'count': 60, 'code': 'BT'},
            'Bio Medical': {'count': 60, 'code': 'BM'},
            'Civil': {'count': 60, 'code': 'CE'},
        }
        
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        Placement.objects.all().delete()
        Student.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        
        # Create companies
        companies_data = [
            {'name': 'TCS', 'location': 'Chennai', 'packages': [3.5, 4.5, 7.0]},
            {'name': 'Infosys', 'location': 'Bangalore', 'packages': [4.0, 5.0, 8.0]},
            {'name': 'Wipro', 'location': 'Hyderabad', 'packages': [3.8, 4.8, 6.5]},
            {'name': 'Cognizant', 'location': 'Chennai', 'packages': [4.2, 5.5, 7.5]},
            {'name': 'Accenture', 'location': 'Bangalore', 'packages': [4.5, 6.0, 9.0]},
            {'name': 'Amazon', 'location': 'Bangalore', 'packages': [15.0, 20.0, 28.0]},
            {'name': 'Google', 'location': 'Bangalore', 'packages': [18.0, 25.0, 35.0]},
            {'name': 'Microsoft', 'location': 'Hyderabad', 'packages': [16.0, 22.0, 30.0]},
            {'name': 'Zoho', 'location': 'Chennai', 'packages': [6.0, 8.0, 12.0]},
            {'name': 'Capgemini', 'location': 'Chennai', 'packages': [4.0, 5.5, 7.0]},
        ]
        
        companies = []
        for comp_data in companies_data:
            company, _ = Company.objects.get_or_create(
                name=comp_data['name'],
                defaults={'location': comp_data['location']}
            )
            companies.append({'obj': company, 'packages': comp_data['packages']})
        
        self.stdout.write(f'Created {len(companies)} companies')
        
        # Create students
        total_students = 0
        total_placements = 0
        year = 2023  # Batch year
        
        for dept_name, dept_info in departments.items():
            count = dept_info['count']
            code = dept_info['code']
            
            self.stdout.write(f'Creating {count} students for {dept_name}...')
            
            for i in range(1, count + 1):
                # Generate roll number: 23CS109 format
                roll_no = f"{year % 100}{code}{i:03d}"
                
                # Create user
                username = f"{roll_no.lower()}"
                user = User.objects.create_user(
                    username=username,
                    email=f"{username}@college.edu",
                    password='student123',
                    first_name=f"Student{i}",
                    last_name=dept_name[:3].upper()
                )
                
                # Generate realistic CGPA (higher for CS branches)
                if dept_name in ['CSE', 'IT', 'CSE(CS)', 'AIML', 'AIDS']:
                    cgpa = round(random.uniform(6.5, 9.8), 2)
                else:
                    cgpa = round(random.uniform(6.0, 9.5), 2)
                
                # Create student
                student = Student.objects.create(
                    user=user,
                    roll_no=roll_no,
                    branch=dept_name,
                    year=4,  # Final year
                    cgpa=cgpa
                )
                
                total_students += 1
                
                # Placement probability based on department and CGPA
                placement_chance = 0.7 if dept_name in ['CSE', 'IT', 'CSE(CS)', 'AIML', 'AIDS'] else 0.5
                if cgpa >= 8.5:
                    placement_chance += 0.2
                elif cgpa >= 7.5:
                    placement_chance += 0.1
                
                # Create placement
                if random.random() < placement_chance:
                    # Select company based on CGPA
                    if cgpa >= 9.0 and dept_name in ['CSE', 'IT', 'CSE(CS)', 'AIML', 'AIDS']:
                        # Top companies for high performers
                        company_data = random.choice(companies[5:9])
                        positions = ['Software Engineer', 'Senior Developer', 'Data Scientist', 'ML Engineer']
                    elif cgpa >= 8.0:
                        # Mid-tier companies
                        company_data = random.choice(companies[3:8])
                        positions = ['Software Developer', 'Associate Engineer', 'Analyst', 'Developer']
                    else:
                        # Mass recruiters
                        company_data = random.choice(companies[0:5])
                        positions = ['Associate', 'Trainee Engineer', 'Junior Developer', 'Graduate Trainee']
                    
                    package = random.choice(company_data['packages'])
                    position = random.choice(positions)
                    
                    # Random date in last 6 months
                    days_ago = random.randint(0, 180)
                    placement_date = date.today() - timedelta(days=days_ago)
                    
                    Placement.objects.create(
                        student=student,
                        company=company_data['obj'],
                        position=position,
                        package_lpa=package,
                        date_offered=placement_date,
                        confirmed=random.choice([True, True, True, False])  # 75% confirmed
                    )
                    
                    total_placements += 1
        
        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Successfully created:'
            f'\n   - {total_students} students across {len(departments)} departments'
            f'\n   - {total_placements} placements ({round(total_placements/total_students*100, 1)}% placement rate)'
            f'\n   - {len(companies)} companies'
        ))
        
        # Show department-wise breakdown
        self.stdout.write('\n📊 Department-wise breakdown:')
        for dept_name in departments.keys():
            dept_students = Student.objects.filter(branch=dept_name).count()
            dept_placements = Placement.objects.filter(student__branch=dept_name).count()
            placement_pct = round(dept_placements/dept_students*100, 1) if dept_students > 0 else 0
            self.stdout.write(f'   {dept_name:12} - {dept_students:3} students, {dept_placements:3} placed ({placement_pct}%)')
