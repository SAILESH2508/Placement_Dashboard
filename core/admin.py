# core/admin.py
from django.contrib import admin
from .models import Student, Company, Placement, Notification, PlacementStatistic

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_no', 'user', 'branch', 'year', 'cgpa')
    search_fields = ('roll_no', 'user__username', 'user__first_name', 'user__last_name')

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'location')

@admin.register(Placement)
class PlacementAdmin(admin.ModelAdmin):
    list_display = ('student', 'company', 'position', 'package_lpa', 'date_offered', 'confirmed')
    list_filter = ('confirmed', 'date_offered')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'pinned')

@admin.register(PlacementStatistic)
class PlacementStatisticAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_placed', 'average_package_lpa')
