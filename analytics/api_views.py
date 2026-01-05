from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from datetime import timedelta
from students.models import Student
from placements.models import Application
import random

class DeptStatsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        stats = Student.objects.values('course').annotate(count=Count('id')).order_by('-count')
        return Response([
            {"name": item['course'], "value": item['count']} for item in stats
        ])

class DailyStatsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        days = int(request.query_params.get('days', 30))
        start_date = timezone.now() - timedelta(days=days)
        
        daily_apps = Application.objects.filter(applied_at__gte=start_date)\
            .annotate(date=TruncDate('applied_at'))\
            .values('date')\
            .annotate(count=Count('id'))\
            .order_by('date')
            
        return Response(daily_apps)

from core.ml_models import predict_single

class PredictMLView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            # Extract features from request
            data = {
                "course": request.data.get('course', 'CSE'),  # course maps to branch
                "branch": request.data.get('branch', 'CSE'),  # backup
                "cgpa": float(request.data.get('cgpa', 7.0)),
                "internships": int(request.data.get('internships', 0)),
                "projects": int(request.data.get('projects', 0)),
                "communication": int(request.data.get('communication', 5)),
                "year": int(request.data.get('year', 2025))
            }
            # Use 'course' as 'branch' if not provided explicitly
            if 'branch' not in request.data and 'course' in request.data:
                data['branch'] = data['course']

            result = predict_single(data)
            
            prob = result['placement_probability'] * 100
            package = result['predicted_package_lpa']
            
            return Response({
                "prediction": "Placed" if prob > 50 else "Not Placed", # Frontend expects "Placed" string
                "confidence": result['placement_probability'], # Frontend expects 0-1
                "status": "High" if prob > 80 else "Medium" if prob > 50 else "Low",
                "predicted_package": f"{package:.2f} LPA",
                "input_features": data
            })
        except Exception as e:
            return Response({"error": str(e)}, status=400)

class ModelMetricsView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        import os
        import json
        from django.conf import settings
        
        METRICS_PATH = os.path.join(settings.BASE_DIR, 'ml_models', 'metrics.json')
        if not os.path.exists(METRICS_PATH):
            return Response({"error": "Metrics not found. Train model first."}, status=404)
            
        with open(METRICS_PATH, 'r') as f:
            data = json.load(f)
        return Response(data)

class RetrainModelView(APIView):
    permission_classes = [permissions.AllowAny] # In production, restrict to Admin only!

    def post(self, request):
        from django.core.management import call_command
        try:
            # Run correctly in sync for now (async is better but requires celery/qcluster)
            call_command('train_ml')
            
            return Response({"status": "Training started and completed successfully", "message": "Model retrained."})
        except Exception as e:
            return Response({"error": str(e)}, status=500)
