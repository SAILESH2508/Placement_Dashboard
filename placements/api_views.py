from rest_framework import generics, permissions, serializers
from .models import Application

class ApplicationSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()
    position = serializers.CharField(source='job.title')
    package_lpa = serializers.SerializerMethodField()
    confirmed = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = ['id', 'student', 'company', 'position', 'package_lpa', 'confirmed']

    def get_student(self, obj):
        return {"roll_no": obj.student.roll_no}

    def get_company(self, obj):
        return {"name": obj.job.company.name}
    
    def get_package_lpa(self, obj):
        import re
        try:
            # Extract number from string like "10 LPA"
            s = str(obj.job.salary)
            val = float(re.sub(r'[^\d.]', '', s))
            return val
        except Exception:
            return 0.0

    def get_confirmed(self, obj):
        return obj.status in ['accepted', 'offered']

class PlacementListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Application.objects.select_related('student', 'job__company').all()
    serializer_class = ApplicationSerializer
