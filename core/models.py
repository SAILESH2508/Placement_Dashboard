# core/models.py
from django.db import models
from django.contrib.auth.models import User

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    roll_no = models.CharField(max_length=32, unique=True)
    branch = models.CharField(max_length=64)
    year = models.IntegerField()
    cgpa = models.DecimalField(max_digits=4, decimal_places=2)
    resume_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.roll_no} - {self.user.get_full_name() if self.user else 'NoName'}"

class Company(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=150, blank=True)
    recruiter_contact = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

class Placement(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='placements')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='placements')
    position = models.CharField(max_length=150)
    package_lpa = models.DecimalField(max_digits=6, decimal_places=2)  # in LPA
    date_offered = models.DateField()
    confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.roll_no} -> {self.company.name} ({self.position})"

class Notification(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    pinned = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class PlacementStatistic(models.Model):
    date = models.DateField()
    total_placed = models.IntegerField()
    average_package_lpa = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('date',)

    def __str__(self):
        return f"{self.date} - {self.total_placed}"
