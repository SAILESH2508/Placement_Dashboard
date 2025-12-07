from django.contrib.auth.models import User
from django.db.models import Count, Avg, Max
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .models import Student, Company, Placement, Notification, PlacementStatistic
from .serializers import (
    StudentSerializer,
    CompanySerializer,
    PlacementSerializer,
    NotificationSerializer,
    PlacementStatisticSerializer,
    RegisterSerializer,
)

from datetime import date, timedelta
from django.db.models.functions import TruncMonth
import logging

logger = logging.getLogger(__name__)


# ================================
# ViewSets
# ================================

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.select_related("user").all()
    serializer_class = StudentSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['roll_no', 'user__username', 'user__first_name', 'user__last_name', 'branch']
    filterset_fields = ['branch', 'year']
    ordering_fields = ['roll_no', 'cgpa', 'year']
    ordering = ['-cgpa']

    @action(detail=False, methods=['get'])
    def top_performers(self, request):
        """Get top performing students by CGPA"""
        limit = int(request.query_params.get('limit', 10))
        students = self.queryset.order_by('-cgpa')[:limit]
        serializer = self.get_serializer(students, many=True)
        return Response(serializer.data)


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]
    search_fields = ['name', 'location']
    ordering_fields = ['name', 'location']
    ordering = ['name']

    @action(detail=True, methods=['get'])
    def placements(self, request, pk=None):
        """Get all placements for a specific company"""
        company = self.get_object()
        placements = Placement.objects.filter(company=company).select_related('student', 'student__user')
        serializer = PlacementSerializer(placements, many=True)
        return Response(serializer.data)


class PlacementViewSet(viewsets.ModelViewSet):
    queryset = Placement.objects.select_related("student", "company").all()
    serializer_class = PlacementSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['confirmed', 'company', 'student']
    ordering_fields = ['date_offered', 'package_lpa']
    ordering = ['-date_offered']

    def perform_create(self, serializer):
        """Add validation when creating placement"""
        try:
            serializer.save()
            logger.info(f"Placement created: {serializer.instance}")
        except Exception as e:
            logger.error(f"Error creating placement: {str(e)}")
            raise ValidationError({"error": "Failed to create placement"})


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all().order_by("-pinned", "-created_at")
    serializer_class = NotificationSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAuthenticated()]


class PlacementStatisticViewSet(viewsets.ModelViewSet):
    queryset = PlacementStatistic.objects.all()
    serializer_class = PlacementStatisticSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        year = self.request.query_params.get("year")
        if year and year != "All":
            qs = qs.filter(date__year=year)
        return qs.order_by("date")


# ================================
# Dashboard Metrics
# ================================

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_metrics(request):
    """Get comprehensive dashboard metrics"""
    try:
        total_placements = Placement.objects.count()
        total_students = Student.objects.count()
        
        placement_stats = Placement.objects.aggregate(
            max_package=Max("package_lpa"),
            avg_package=Avg("package_lpa")
        )
        
        return Response({
            "total_students": total_students,
            "total_companies": Company.objects.count(),
            "total_placements": total_placements,
            "unique_placed_students": Placement.objects.values("student").distinct().count(),
            "placement_percentage": round((Placement.objects.values("student").distinct().count() / total_students * 100), 2) if total_students > 0 else 0,
            "best_package_lpa": float(placement_stats["max_package"] or 0),
            "average_package_lpa": round(float(placement_stats["avg_package"] or 0), 2),
        })
    except Exception as e:
        logger.error(f"Error fetching dashboard metrics: {str(e)}")
        return Response({"error": "Failed to fetch metrics"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([AllowAny])
def dashboard_summary(request):
    return Response({
        "total_students": Student.objects.count(),
        "total_companies": Company.objects.count(),
        "total_placements": Placement.objects.count(),
    })


# ================================
# Statistics Endpoints
# ================================

@api_view(["GET"])
def monthly_statistics(request):
    year = request.query_params.get("year")

    qs = Placement.objects.all()
    if year and year != "All":
        qs = qs.filter(date_offered__year=year)

    data = (
        qs.annotate(month=TruncMonth("date_offered"))
        .values("month")
        .annotate(
            total_placements=Count("id"),
            avg_package_lpa=Avg("package_lpa"),
        )
        .order_by("month")
    )

    return Response({
        "results": [
            {
                "month": d["month"].strftime("%Y-%m"),
                "total_placements": d["total_placements"],
                "avg_package_lpa": round(d["avg_package_lpa"] or 0, 2),
            }
            for d in data
        ]
    })


@api_view(["GET"])
def department_statistics(request):
    year = request.query_params.get("year")

    qs = Placement.objects.select_related("student")
    if year and year != "All":
        qs = qs.filter(date_offered__year=year)

    data = (
        qs.values("student__branch")
        .annotate(total_placed=Count("id"))
        .order_by("student__branch")
    )

    return Response({
        "results": [
            {
                "department": d["student__branch"],
                "placed": d["total_placed"],
            }
            for d in data
        ]
    })


@api_view(["GET"])
def daily_statistics(request):
    days = int(request.query_params.get("days", 30))
    start = date.today() - timedelta(days=days)

    qs = Placement.objects.filter(date_offered__gte=start)

    data = (
        qs.values("date_offered")
        .annotate(total=Count("id"))
        .order_by("date_offered")
    )

    return Response({
        "results": [
            {
                "date": d["date_offered"].strftime("%Y-%m-%d"),
                "placed": d["total"],
            }
            for d in data
        ]
    })


# ================================
# Registration / Forgot Password
# ================================

@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        # Create minimal student record
        Student.objects.create(
            user=user,
            roll_no=f"AUTO{user.id}",
            branch="CSE",
            year=1,
            cgpa=0.0
        )

        return Response({"message": "User registered successfully"}, status=201)

    return Response(serializer.errors, status=400)


@api_view(["POST"])
@permission_classes([AllowAny])
def forgot_password(request):
    email = request.data.get("email")
    if not email:
        return Response({"error": "Email is required"}, status=400)
    return Response({"message": "Password reset instructions sent"})


# ================================
# Top Companies (Final Improved Version)
# ================================

@api_view(["GET"])
@permission_classes([AllowAny])
def top_companies(request):
    limit = int(request.query_params.get("limit", 5))
    year = request.query_params.get("year")
    branch = request.query_params.get("branch")

    qs = Placement.objects.select_related("company", "student")

    if year and year != "All":
        qs = qs.filter(date_offered__year=year)

    if branch and branch != "All":
        qs = qs.filter(student__branch__iexact=branch)

    ranking = (
        qs.values("company__id", "company__name")
        .annotate(
            total_placements=Count("id"),
            avg_package=Avg("package_lpa"),
            max_package=Max("package_lpa")
        )
        .order_by("-total_placements")[:limit]
    )

    trend = (
        qs.annotate(month=TruncMonth("date_offered"))
        .values("company__name", "month")
        .annotate(count=Count("id"))
        .order_by("company__name", "month")
    )

    return Response({
        "ranking": [
            {
                "company": r["company__name"],
                "total_placements": r["total_placements"],
                "avg_package_lpa": round(r["avg_package"] or 0, 2),
                "max_package_lpa": round(r["max_package"] or 0, 2),
            }
            for r in ranking
        ],
        "trend": [
            {
                "company": t["company__name"],
                "month": t["month"].strftime("%Y-%m"),
                "placed": t["count"],
            }
            for t in trend
        ]
    })
