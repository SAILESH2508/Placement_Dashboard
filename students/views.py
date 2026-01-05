import json
from django.db import models
from django.shortcuts import render, get_object_or_404
from students.models import Student
from companies.models import Company
from placements.models import Job, Application
from notifications.models import Notification
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    students_count = Student.objects.count()
    companies_count = Company.objects.count()
    jobs_count = Job.objects.filter(is_active=True).count()
    applications_count = Application.objects.count()
    recent_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:5]

    # simple stats for charts
    status_counts = Application.objects.values('status').order_by().annotate(count=models.Count('id'))
    status_counts_list = list(status_counts)

    context = {
        'students_count': students_count,
        'companies_count': companies_count,
        'jobs_count': jobs_count,
        'applications_count': applications_count,
        'recent_notifications': recent_notifications,
        'status_counts': status_counts_list,
        'status_counts_json': json.dumps(status_counts_list),
    }
    return render(request, 'dashboard.html', context)

def student_list(request):
    students = Student.objects.select_related('user').all()
    return render(request, 'students/list.html', {'students': students})

def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'students/detail.html', {'student': student})
