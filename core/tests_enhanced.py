"""
Enhanced test cases for the placement portal
Run with: python manage.py test core.tests_enhanced
"""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import date, timedelta
from decimal import Decimal

from .models import Student, Company, Placement, Notification
from .serializers import StudentSerializer, CompanySerializer, PlacementSerializer


class StudentModelTest(TestCase):
    """Test cases for Student model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_create_student(self):
        """Test creating a student"""
        student = Student.objects.create(
            user=self.user,
            roll_no='2021CSE001',
            branch='CSE',
            year=4,
            cgpa=Decimal('8.50')
        )
        self.assertEqual(student.roll_no, '2021CSE001')
        self.assertEqual(student.branch, 'CSE')
        self.assertEqual(student.cgpa, Decimal('8.50'))
        
    def test_student_str_representation(self):
        """Test student string representation"""
        student = Student.objects.create(
            user=self.user,
            roll_no='2021CSE001',
            branch='CSE',
            year=4,
            cgpa=Decimal('8.50')
        )
        expected = f"2021CSE001 - {self.user.get_full_name()}"
        self.assertEqual(str(student), expected)


class CompanyModelTest(TestCase):
    """Test cases for Company model"""
    
    def test_create_company(self):
        """Test creating a company"""
        company = Company.objects.create(
            name='Google',
            description='Tech company',
            website='https://google.com',
            location='Bangalore'
        )
        self.assertEqual(company.name, 'Google')
        self.assertEqual(company.location, 'Bangalore')
        
    def test_company_str_representation(self):
        """Test company string representation"""
        company = Company.objects.create(name='Microsoft')
        self.assertEqual(str(company), 'Microsoft')


class PlacementModelTest(TestCase):
    """Test cases for Placement model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.student = Student.objects.create(
            user=self.user,
            roll_no='2021CSE001',
            branch='CSE',
            year=4,
            cgpa=Decimal('8.50')
        )
        self.company = Company.objects.create(name='Google')
        
    def test_create_placement(self):
        """Test creating a placement"""
        placement = Placement.objects.create(
            student=self.student,
            company=self.company,
            position='Software Engineer',
            package_lpa=Decimal('15.00'),
            date_offered=date.today(),
            confirmed=True
        )
        self.assertEqual(placement.position, 'Software Engineer')
        self.assertEqual(placement.package_lpa, Decimal('15.00'))
        self.assertTrue(placement.confirmed)


class AuthenticationAPITest(APITestCase):
    """Test cases for authentication endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.register_url = '/api/auth/register/'
        self.login_url = '/api/auth/login/'
        self.me_url = '/api/auth/me/'
        
    def test_user_registration(self):
        """Test user registration"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'securepass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)
        
    def test_registration_duplicate_username(self):
        """Test registration with duplicate username"""
        User.objects.create_user(username='existing', password='pass123')
        data = {
            'username': 'existing',
            'email': 'new@example.com',
            'password': 'pass123'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_registration_weak_password(self):
        """Test registration with weak password"""
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'weak'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_user_login(self):
        """Test user login"""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)
        
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        data = {
            'username': 'nonexistent',
            'password': 'wrongpass'
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_get_current_user(self):
        """Test getting current user info"""
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=user)
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')


class StudentAPITest(APITestCase):
    """Test cases for student endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.student_url = '/api/students/'
        
    def test_list_students(self):
        """Test listing students"""
        response = self.client.get(self.student_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_create_student(self):
        """Test creating a student"""
        data = {
            'roll_no': '2021CSE001',
            'branch': 'CSE',
            'year': 4,
            'cgpa': 8.5
        }
        response = self.client.post(self.student_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_create_student_invalid_cgpa(self):
        """Test creating student with invalid CGPA"""
        data = {
            'roll_no': '2021CSE001',
            'branch': 'CSE',
            'year': 4,
            'cgpa': 11.0  # Invalid: > 10
        }
        response = self.client.post(self.student_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PlacementAPITest(APITestCase):
    """Test cases for placement endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.student = Student.objects.create(
            user=self.user,
            roll_no='2021CSE001',
            branch='CSE',
            year=4,
            cgpa=Decimal('8.50')
        )
        self.company = Company.objects.create(name='Google')
        self.placement_url = '/api/placements/'
        
    def test_create_placement(self):
        """Test creating a placement"""
        data = {
            'student_id': self.student.id,
            'company_id': self.company.id,
            'position': 'Software Engineer',
            'package_lpa': 15.0,
            'date_offered': date.today().isoformat(),
            'confirmed': True
        }
        response = self.client.post(self.placement_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_create_placement_invalid_package(self):
        """Test creating placement with invalid package"""
        data = {
            'student_id': self.student.id,
            'company_id': self.company.id,
            'position': 'Software Engineer',
            'package_lpa': -5.0,  # Invalid: negative
            'date_offered': date.today().isoformat(),
            'confirmed': True
        }
        response = self.client.post(self.placement_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class StatisticsAPITest(APITestCase):
    """Test cases for statistics endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        # Create test data
        self.student = Student.objects.create(
            user=self.user,
            roll_no='2021CSE001',
            branch='CSE',
            year=4,
            cgpa=Decimal('8.50')
        )
        self.company = Company.objects.create(name='Google')
        Placement.objects.create(
            student=self.student,
            company=self.company,
            position='Software Engineer',
            package_lpa=Decimal('15.00'),
            date_offered=date.today()
        )
        
    def test_dashboard_metrics(self):
        """Test dashboard metrics endpoint"""
        response = self.client.get('/api/metrics/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_students', response.data)
        self.assertIn('total_placements', response.data)
        self.assertIn('placement_percentage', response.data)
        
    def test_monthly_statistics(self):
        """Test monthly statistics endpoint"""
        response = self.client.get('/api/statistics/monthly/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)


class MLPredictionAPITest(APITestCase):
    """Test cases for ML prediction endpoint"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        self.predict_url = '/api/ml/predict/'
        
    def test_valid_prediction(self):
        """Test ML prediction with valid data"""
        data = {
            'cgpa': 8.5,
            'internships': 2,
            'projects': 3,
            'communication': 8
        }
        response = self.client.post(self.predict_url, data)
        # May fail if model not trained, but should return proper error
        self.assertIn(response.status_code, [
            status.HTTP_200_OK,
            status.HTTP_503_SERVICE_UNAVAILABLE
        ])
        
    def test_prediction_invalid_cgpa(self):
        """Test prediction with invalid CGPA"""
        data = {
            'cgpa': 11.0,  # Invalid: > 10
            'internships': 2,
            'projects': 3,
            'communication': 8
        }
        response = self.client.post(self.predict_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_prediction_missing_fields(self):
        """Test prediction with missing fields"""
        data = {
            'cgpa': 8.5
            # Missing other required fields
        }
        response = self.client.post(self.predict_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SerializerTest(TestCase):
    """Test cases for serializers"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.student = Student.objects.create(
            user=self.user,
            roll_no='2021CSE001',
            branch='CSE',
            year=4,
            cgpa=Decimal('8.50')
        )
        
    def test_student_serializer(self):
        """Test student serializer"""
        serializer = StudentSerializer(self.student)
        self.assertEqual(serializer.data['roll_no'], '2021CSE001')
        self.assertIn('user', serializer.data)
        self.assertIn('placement_count', serializer.data)
        
    def test_student_serializer_validation(self):
        """Test student serializer validation"""
        data = {
            'roll_no': '2021CSE002',
            'branch': 'CSE',
            'year': 4,
            'cgpa': 11.0  # Invalid
        }
        serializer = StudentSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('cgpa', serializer.errors)


# Run tests with:
# python manage.py test core.tests_enhanced
# python manage.py test core.tests_enhanced.AuthenticationAPITest
# python manage.py test core.tests_enhanced.StudentAPITest.test_create_student
