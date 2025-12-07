# core/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Student, Company, Placement, Notification, PlacementStatistic


# --- User Serializer ---
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


# --- Student Serializer ---
class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    placement_count = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = '__all__'

    def get_placement_count(self, obj):
        """Get number of placements for this student"""
        return obj.placements.count()

    def validate_cgpa(self, value):
        """Validate CGPA is in valid range"""
        if value < 0 or value > 10:
            raise serializers.ValidationError("CGPA must be between 0 and 10")
        return value

    def validate_year(self, value):
        """Validate year is reasonable"""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Year must be between 1 and 5")
        return value


# --- Company Serializer ---
class CompanySerializer(serializers.ModelSerializer):
    total_placements = serializers.SerializerMethodField()
    average_package = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = '__all__'

    def get_total_placements(self, obj):
        """Get total number of placements from this company"""
        return obj.placements.count()

    def get_average_package(self, obj):
        """Get average package offered by this company"""
        from django.db.models import Avg
        avg = obj.placements.aggregate(Avg('package_lpa'))['package_lpa__avg']
        return round(float(avg), 2) if avg else 0


# --- Simple Serializers for List Views ---
class SimpleStudentSerializer(serializers.ModelSerializer):
    """Lightweight student serializer for nested use"""
    class Meta:
        model = Student
        fields = ['id', 'roll_no', 'branch', 'year', 'cgpa']


class SimpleCompanySerializer(serializers.ModelSerializer):
    """Lightweight company serializer for nested use"""
    class Meta:
        model = Company
        fields = ['id', 'name', 'location']


# --- Placement Serializer ---
class PlacementSerializer(serializers.ModelSerializer):
    student = SimpleStudentSerializer(read_only=True)
    company = SimpleCompanySerializer(read_only=True)
    student_id = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(), 
        source='student', 
        write_only=True
    )
    company_id = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(), 
        source='company', 
        write_only=True
    )

    class Meta:
        model = Placement
        fields = '__all__'

    def validate_package_lpa(self, value):
        """Validate package is positive"""
        if value <= 0:
            raise serializers.ValidationError("Package must be greater than 0")
        if value > 200:  # Reasonable upper limit
            raise serializers.ValidationError("Package seems unrealistically high")
        return value

    def validate(self, data):
        """Check for duplicate placements"""
        student = data.get('student')
        company = data.get('company')
        
        if student and company:
            # Check if this student already has a placement with this company
            existing = Placement.objects.filter(
                student=student, 
                company=company
            ).exclude(pk=self.instance.pk if self.instance else None)
            
            if existing.exists():
                raise serializers.ValidationError(
                    "This student already has a placement record with this company"
                )
        
        return data


# --- Notification Serializer ---
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


# --- Placement Statistic Serializer ---
class PlacementStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlacementStatistic
        fields = '__all__'


# --- User Registration Serializer ---
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user
