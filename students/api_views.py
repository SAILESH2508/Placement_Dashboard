from rest_framework import generics, permissions, serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    branch = serializers.CharField(source='course')
    resume_link = serializers.FileField(source='resume', use_url=True)

    class Meta:
        model = Student
        fields = ['id', 'username', 'email', 'roll_no', 'course', 'branch', 'year', 'cgpa', 'resume_link']

class StudentListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Student.objects.all().select_related('user')
    serializer_class = StudentSerializer
