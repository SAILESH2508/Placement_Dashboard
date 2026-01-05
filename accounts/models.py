from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
        ('company', 'Company'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    # optional extra fields
    phone = models.CharField(max_length=20, blank=True, null=True)
    college = models.CharField(max_length=255, blank=True, null=True)

    def is_student(self):
        return self.role == 'student'

    def is_company(self):
        return self.role == 'company'

    def is_admin_account(self):
        return self.role == 'admin'
