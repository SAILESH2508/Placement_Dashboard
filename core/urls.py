from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    StudentViewSet,
    CompanyViewSet,
    PlacementViewSet,
    NotificationViewSet,
    PlacementStatisticViewSet,
    dashboard_metrics,
    dashboard_summary,
    daily_statistics,
    monthly_statistics,
    department_statistics,
    top_companies,
)

router = DefaultRouter()
router.register("students", StudentViewSet)
router.register("companies", CompanyViewSet)
router.register("placements", PlacementViewSet)
router.register("notifications", NotificationViewSet)
router.register("placement-statistics", PlacementStatisticViewSet)

urlpatterns = [
    # Custom endpoints BEFORE router (to avoid conflicts)
    path("dashboard/summary/", dashboard_summary),
    path("metrics/", dashboard_metrics),

    # Stats
    path("statistics/daily/", daily_statistics),
    path("statistics/monthly/", monthly_statistics),
    path("statistics/dept/", department_statistics),

    # Top companies endpoint (must come before router)
    path("companies/top/", top_companies),

    # Router URLs (must come last)
    path("", include(router.urls)),
]
