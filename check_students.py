import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'placement_portal.settings')
django.setup()

from core.models import Student
from django.db.models import Count

print(f"Total students: {Student.objects.count()}\n")
print("Department-wise breakdown:")
print("-" * 40)

depts = Student.objects.values('branch').annotate(count=Count('id')).order_by('branch')
for dept in depts:
    print(f"{dept['branch']:15} - {dept['count']:3} students")
