from django.db import models
from students.models import Student
from companies.models import Company

class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    salary = models.CharField(max_length=100, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    application_deadline = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} @ {self.company.name}"

class Application(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applied_at = models.DateTimeField(auto_now_add=True)
    status_choices = [
        ('applied','Applied'),
        ('shortlisted','Shortlisted'),
        ('interview','Interview'),
        ('offered','Offered'),
        ('rejected','Rejected'),
        ('accepted','Accepted'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='applied')
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('student', 'job')

    def __str__(self):
        return f"{self.student} -> {self.job} ({self.status})"
