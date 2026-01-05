from rest_framework import generics, permissions, views
from rest_framework.response import Response
from .models import Company

from rest_framework import serializers

class CompanySerializer(serializers.ModelSerializer):
    location = serializers.CharField(source='city')
    recruiter_contact = serializers.CharField(source='contact_email')

    class Meta:
        model = Company
        fields = '__all__'

class TopCompaniesView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CompanySerializer

    def get_queryset(self):
        limit = int(self.request.query_params.get('limit', 7))
        # Logic to get "top" companies, for now just first N
        return Company.objects.all()[:limit]

class CompanyListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
