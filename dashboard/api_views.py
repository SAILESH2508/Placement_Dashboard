from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from students.models import Student
from companies.models import Company
from placements.models import Job, Application

class DashboardSummaryView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        student_count = Student.objects.count()
        company_count = Company.objects.count()
        job_count = Job.objects.count()
        
        # specific logic for "placed" could be status='accepted' or 'offered'
        placed_count = Application.objects.filter(status__in=['accepted', 'offered']).count()
        
        # Calculate Average Package
        from django.db.models import Avg
        avg_package = Application.objects.filter(status__in=['accepted', 'offered']).aggregate(Avg('job__salary'))['job__salary__avg']
        
        # Determine strict numeric value for average (cleanup string if needed or rely on database)
        # Since job.salary is a CharField, we might need python-side calc or safe conversion if DB is mixed.
        # But for now, let's assume we can get it or compute it from accepted apps.
        
        total_salary = 0
        count = 0
        accepted_apps = Application.objects.filter(status__in=['accepted', 'offered']).select_related('job')
        import re
        for app in accepted_apps:
            try:
                s = str(app.job.salary)
                val = float(re.sub(r'[^\d.]', '', s))
                total_salary += val
                count += 1
            except:
                pass
        
        avg_val = (total_salary / count) if count > 0 else 0.0

        return Response({
            "total_students": student_count,
            "total_companies": company_count,
            "total_jobs": job_count,
            "total_placements": placed_count,
            "avg_package_lpa": round(avg_val, 2)
        })
